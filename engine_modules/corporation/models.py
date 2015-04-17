# -*- coding: utf-8 -*-
import random
from os import listdir
from collections import OrderedDict

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

from utils.read_markdown import read_markdown
from engine_modules.market.models import Market, CorporationMarket
from engine.models import Game

class BaseCorporation:
	"""
	Basic corporation definition, reused for each game
	Implemented as a separate non-model class to avoid cluttering the database
	"""

	BASE_CORPORATION_TEMPLATE = "%s/corporations"
	BASE_CORPORATION_DIR = BASE_CORPORATION_TEMPLATE % (settings.CITY_BASE_DIR)

	@classmethod
	def build_dict(cls):
		"""
		Build a dict holding all base corporations.
		This dict is static and will be available anytime.
		"""
		cls.base_corporations = {}
		for f in [f for f in listdir(cls.BASE_CORPORATION_DIR) if f.endswith('.md')]:
			bc = BaseCorporation(f[:-3])  # f[:-3] is the slug
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

		code = "\n".join(meta['on_crash'])
		self.on_crash = self.compile_effect(code, "on_crash")

		self.initials_assets = 0
		self.markets = OrderedDict()
		markets = meta['markets']
		for market in markets[1:]:
			name, value = market.split(": ")
			self.markets[name] = int(value)
			self.initials_assets += int(value)

	def compile_effect(self, code, effect):
		"""
		Compile specified code. Second parameter is a string that will be used for stacktrace reports.
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
	market_assets = models.SmallIntegerField()
	assets_modifier = models.SmallIntegerField(default=0)

	@property
	def corporation_markets(self):
		"""
		Returns all CorporationMarket objects associated with the Corporation
		"""
		return self.corporationmarket_set.all()

	@property
	def markets(self):
		"""
		Returns all Market objects associated with the Corporation
		"""
		return [cm.market for cm in self.corporation_markets]

	@property
	def random_corporation_market(self):
		"""
		Returns one object at random among the CorporationMarket objects associated with the Corporation
		"""
		return random.choice(self.corporation_markets)

	def get_random_market(self):
		"""
		Returns one object at random among the Market objects associated with the Corporation
		"""
		return random.choice(self.markets)

	def get_common_corporation_market(self, c2):
		"""
		Returns the CorporationMaket for a common market between the Corporation and c2 if there is one.
		Raises a ValidationError otherwise, because two Corporations should have at least one common Market.
		"""
		c2_markets = c2.markets
		common_corporation_markets = [cm for cm in self.corporation_markets if cm.market in c2_markets]
		
		if len(common_corporation_markets) != 0:
			return random.choice(common_corporation_markets)
		else:
			raise ValidationError("Corporations %s and %s have no common market" % (self.base_corporation.name, c2.base_corporation.name))

	@cached_property
	def base_corporation(self):
		return BaseCorporation.base_corporations[self.base_corporation_slug]

	def apply_effect(self, code, delta_category, ladder):
		"""
		Applies the effect described in code with respect to the ladder, in category delta_category
		"""
		def update(corporation, delta, market=None):
			"""
			Updates corporation's assets by delta, in Market market if specified, or a Market at random otherwise
			"""
			if isinstance(corporation, str):
				# Try / catch if corporation crashed
				try:
					corporation = self.game.corporation_set.get(base_corporation_slug=corporation)
				except Corporation.DoesNotExist:
					return

			if market is None:
				# By default, a random market is impacted
				market = corporation.get_random_market()
			else:
				# TODO; implement and test effects with a market name
				raise NotImplementedError()

			corporation.update_assets(delta, category=delta_category, market=market)

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

	def on_crash_effect(self, ladder):
		self.apply_effect(self.base_corporation.on_crash, AssetDelta.EFFECT_CRASH, ladder)

	def increase_assets(self, value=1):
		"""
		Increase corporation's assets by value
		"""
		self.market_assets += value
		self.save()

	def decrease_assets(self, value=1):
		"""
		Decrease corporation's assets by value
		"""

		self.market_assets -= value
		self.save()

	def update_assets(self, delta, category, market):
		"""
		Update assets values, and save the model
		"""
		market = self.corporationmarket_set.get(market=market)

		# A market can't be negative, so we cap the delta
		if market.value + delta < 0:
			# A market can't be negative, so we cap the delta
			delta = -market.value

		market.value += delta
		market.save()

		# Mirror changes on assets
		self.assets += delta
		self.save()

		# And register assetdelta for logging purposes
		self.assetdelta_set.create(category=category, delta=delta, turn=self.game.current_turn)

	def __unicode__(self):
		return "%s (%s)" % (self.base_corporation.name, self.assets)


class AssetDelta(models.Model):
	"""
	Store delta for assets
	"""
	EFFECT_FIRST = 'effect-first'
	EFFECT_LAST = 'effect-last'
	EFFECT_CRASH = 'effect-crash'
	RUN_SABOTAGE = 'sabotage'
	RUN_EXTRACTION = 'extraction'
	RUN_DATASTEAL = 'datasteal'
	DINC = 'detroit-inc'
	INVISIBLE_HAND = 'invisible-hand'
	VOTES = 'votes'

	CATEGORY_CHOICES = (
		(EFFECT_FIRST, 'Eff. premier'),
		(EFFECT_LAST, 'Eff. dernier'),
		(EFFECT_CRASH, 'Eff. crash'),
		(DINC, 'Detroit, Inc.'),
		(RUN_SABOTAGE, 'Sabotage'),
		(RUN_EXTRACTION, 'Extraction'),
		(RUN_DATASTEAL, 'Datasteal'),
		(INVISIBLE_HAND, 'Main Invisible'),
		(VOTES, 'Votes'),
	)

	"""
	Data to be publicly displayed at any time.
	"""
	PUBLIC_DELTA = (
		EFFECT_FIRST,
		EFFECT_LAST,
		EFFECT_CRASH,
		RUN_SABOTAGE,
		DINC
	)

	category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
	corporation = models.ForeignKey(Corporation)
	delta = models.SmallIntegerField()
	turn = models.SmallIntegerField(default=0)
