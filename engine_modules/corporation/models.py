# -*- coding: utf-8 -*-
from os import listdir

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from collections import OrderedDict

from utils.read_markdown import read_markdown
from engine_modules.market.models import Market
from engine.models import Game


class BaseCorporation:
	"""
	Basic corporation definition, reused for each game
	Implemented as a separate non-model class to avoid cluttering the database
	"""

	BASE_CORPORATION_DIR = "%s/corporations" % (settings.CITY_BASE_DIR)

	@classmethod
	def build_dict(cls):
		"""
		Build a dict holding all base corporations.
		This dict is static and will be available anytime.
		"""
		cls.base_corporations = {}
		for f in [f for f in listdir(cls.BASE_CORPORATION_DIR) if f.endswith('.md')]:
			bc = BaseCorporation(f[:-3])
			cls.base_corporations[bc.slug] = bc

	def __init__(self, slug):
		"""
		Create a base_corporation from a file
		"""
		path = "%s/%s.md" % (self.BASE_CORPORATION_DIR, slug)
		content, meta = read_markdown(path)
		self.meta = meta

		self.slug = slug
		self.name = meta['name'][0]
		self.description = mark_safe(content)

		self.datasteal = int(meta['datasteal'][0])
		self.sabotage = int(meta['sabotage'][0])
		self.extraction = int(meta['extraction'][0])
		self.detection = int(meta['detection'][0])

		code = "\n".join(meta['on_first'])
		self.on_first = self.compile_effect(code, "on_first")

		code = "\n".join(meta['on_last'])
		self.on_last = self.compile_effect(code, "on_last")

		self.initials_assets = 0
		self.market = OrderedDict()
		markets = meta['markets']
		for market in markets[1:]:
			name, value = market.split(" - ")
			self.market[name] = int(value)
			self.initials_assets += int(value)
		self.historic_market = self.market.keys()[0]

	def compile_effect(self, code, effect):
		"""
		Compile specified code. Effect is a string that will be used for stacktrace reports.
		"""
		return compile(code, "%s.%s()" % (self.name, effect), 'exec')

	@classmethod
	def retrieve_all(cls):
		return cls.base_corporations.values()

# Build the dict at startup once and for all
BaseCorporation.build_dict()


class Corporation(models.Model):
	"""
	A corporation being part of a game
	"""
	class Meta:
		unique_together = (('base_corporation_slug', 'game'), )
		ordering = ['base_corporation_slug']

	base_corporation_slug = models.CharField(max_length=20)
	game = models.ForeignKey(Game)
	assets = models.SmallIntegerField()
	historic_market = models.ForeignKey(Market)

	@cached_property
	def base_corporation(self):
		return BaseCorporation.base_corporations[self.base_corporation_slug]

	def apply_effect(self, code, delta_category, ladder):

		def update(corporation, delta):
			if isinstance(corporation, str):
				# Try / catch if corporation crashed
				try:
					corporation = self.game.corporation_set.get(base_corporation_slug=corporation)
				except Corporation.DoesNotExist:
					return

			corporation.update_assets(delta, category=delta_category)

		context = {
			'game': self.game,
			'ladder': ladder,
			'update': update
		}

		exec code in {}, context

	def on_first_effect(self, ladder):
		self.apply_effect(self.base_corporation.on_first, AssetDelta.EFFECT_FIRST, ladder)

	def on_last_effect(self, ladder):
		self.apply_effect(self.base_corporation.on_last, AssetDelta.EFFECT_LAST, ladder)

	def update_assets(self, delta, market=None, category=None):
		"""
		Update assets values, and save the model
		"""
		if market is None:
			market = self.historic_market

		market = self.corporationmarket_set.get(market=market)

		if market.value + delta < 0:
			# A market can't be negative, so we cap the delta
			delta = -market.value

		market.value += delta
		market.save()

		# Mirror changes on assets
		self.assets += delta
		self.save()

		if category is not None:
			self.assetdelta_set.create(category=category, delta=delta, turn=self.game.current_turn)

	def __unicode__(self):
		return "%s (%s)" % (self.base_corporation.name, self.assets)


class AssetDelta(models.Model):
	"""
	Store delta for assets
	"""
	EFFECT_FIRST = 'effect-first'
	EFFECT_LAST = 'effect-last'
	RUN_SABOTAGE = 'sabotage'
	RUN_EXTRACTION = 'extraction'
	MDC = 'mdc'

	CATEGORY_CHOICES = (
		(EFFECT_FIRST, 'Eff. premier'),
		(EFFECT_LAST, 'Eff. dernier'),
		(RUN_SABOTAGE, 'Sabotage'),
		(RUN_EXTRACTION, 'Extraction'),
		(MDC, 'MDC'),
	)

	category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
	corporation = models.ForeignKey(Corporation)
	delta = models.SmallIntegerField()
	turn = models.SmallIntegerField(default=0)

	def get_category_shortcut(self):
		return dict(AssetDelta.SHORTCUTS)[self.category]
