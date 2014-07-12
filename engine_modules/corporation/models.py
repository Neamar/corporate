# -*- coding: utf-8 -*-
from os import listdir

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from utils.read_markdown import read_markdown
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
		self.market = {}
		marches = meta['market']	
		for s in marches[1:]:
			s = s.split(" - ")
			self.market[s[0]] = int(s[1])
			self.initials_assets += int(s[1])

		try:
			self.derivative = meta['derivative'][0]
		except KeyError:
			self.derivative = None

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

	def update_assets(self, delta, category=None):
		"""
		Update assets values, and save the model
		"""
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
