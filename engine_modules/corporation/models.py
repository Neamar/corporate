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
		self.phoenix = int(meta['phoenix'][0])

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
		return compile(code, "%s.%s()" % (self.slug, effect), 'exec')

	@classmethod
	def retrieve_all(cls):
		return cls.base_corporations.values()

# Build the dict at startup once and for all
# This is executed when the file is imported (this is why 'import from' is important) !
# Isn't there a better way to do this ?
BaseCorporation.build_dict()


class Corporation(models.Model):
	"""
	A corporation being part of a game
	"""
	class Meta:
		unique_together = (('base_corporation_slug', 'game'), )
		ordering = ['base_corporation_slug']

	base_corporation_slug = models.CharField(max_length=20)
	# We change the related name of game object so we can do game.all_corporation_set to get all the corporation and game.corporation_set to have only a filtered queryset
	# Note that corporation_set is defined on the game as all_corporation_set.filter...
	game = models.ForeignKey(
		Game,
		related_name="all_corporation_set"
	)
	# assets, market_assets and assets_modifier are meant to keep track of the bubbles:
	# - market_assets stands for the total of the assets in the Corporation's markets disregarding bubbles.
	# - assets_modifier stands for the bonuses and maluses originating from domination on a market, or having a market at 0 asset.
	# - assets stands for the assets that must be usually taken into account, so we have: assets = market_assets + assets_modifier
	assets = models.SmallIntegerField()
	market_assets = models.SmallIntegerField()
	assets_modifier = models.SmallIntegerField(default=0)
	# We do a logical delete rather than a real one to avoid reference problems to a crashed corporation
	# Furthermore, we save the turn a corporation have crashed in order to continue seeing it at a turn
	# In the game, corporation_set will be overwrite to filter on corporation that hasn't crashed yet plus coproration that crashed this turn
	crash_turn = models.SmallIntegerField(null=True, blank=True)

	@property
	def corporation_markets(self):
		"""
		Returns all CorporationMarket objects associated with the Corporation for the current turn
		"""
		return self.get_corporation_markets()

	def get_corporation_markets(self, turn=None):
		"""
		Returns all CorporationMarket objects associated with the Corporation for the specified turn
		"""
		if turn is None:
			turn = self.game.current_turn
		return self.corporationmarket_set.filter(turn=turn)

	@property
	def markets(self):
		"""
		Returns all Market objects associated with the Corporation for the current turn
		"""
		return self.get_markets()

	def get_markets(self, turn=None):
		"""
		Returns all Market objects associated with the Corporation for the current turn
		"""
		# The case where turn is None is handled by get_corporation_markets
		return [cm.market for cm in self.get_corporation_markets(turn)]

	def get_random_corporation_market(self):
		"""
		Returns one object at random among the CorporationMarket objects associated with the Corporation
		"""
		return random.choice(self.corporation_markets)

	def get_random_corporation_market_among_bests(self):
		"""
		Return the CorporationMarket with the higher asset among corporationMarket of this corporation.
		If there are som ex-aequo, pick at random among them
		"""
		cms = list(self.corporation_markets.order_by('-value'))
		max_value = cms[0]
		for cm in cms:
			if cm.value < max_value:
				cms.remove(cm)

		return random.choice(cms)

	def get_random_market(self):
		"""
		Returns one object at random among the Market objects associated with the Corporation
		"""
		return random.choice(self.markets)

	def get_common_corporation_market(self, c2):
		"""
		Returns the CorporationMarket object for a common market between the Corporation and c2 if there is one
		Raises a ValidationError otherwise, because two Corporations should have at least one common Market
		This does not actually return a common CorporationMarket, because there is no such thing: a CorporationMarket is by definition specific to a Corporation
		"""

		return random.choice(self.get_common_corporation_markets(c2))

	def get_common_corporation_markets(self, c2):
		"""
		Returns a list of CorporationMarket objects for every common market between the Corporation and c2 if there is one.
		Raises ValidationError otherwise.
		"""
		c2_markets = c2.markets
		common_corporation_markets = [cm for cm in self.corporation_markets if cm.market in c2_markets]
		if len(common_corporation_markets) == 0:
			raise ValidationError("Corporations %s and %s have no common market" % (self.base_corporation.name, c2.base_corporation.name))
		else:
			return common_corporation_markets

	def get_common_market(self, c2):
		"""
		Returns the Market object for a common market between the Corporation if there is at least one
		Raises a ValidationError otherwise, because two Corporations should have at least one common Market
		"""
		return self.get_common_corporation_market(c2).market

	def get_common_markets(self, c2):
		"""
		Returns a list of Market objects for every common market between the Corporation and c2 if there is one.
		Raises ValidationError otherwise.
		"""
		common_corporation_markets = self.get_common_corporation_markets(c2)
		return [cm.market for cm in common_corporation_markets]

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
				# Try / catch if corporation does not exists
				try:
					corporation = self.game.corporation_set.get(base_corporation_slug=corporation, crash_turn__isnull=True)
				except Corporation.DoesNotExist:
					return

			if market is None:
				# By default, the higher market is impacted
				corporation_market = corporation.get_random_corporation_market_among_bests()
			else:
				corporation_market = corporation.corporationmarket_set.get(market__name=market, turn=self.game.current_turn)

			corporation.update_assets(delta, category=delta_category, corporation_market=corporation_market)

			# create a event_type
			if delta_category == AssetDelta.EFFECT_FIRST:
				event_type = Game.FIRST_EFFECT
			elif delta_category == AssetDelta.EFFECT_LAST:
				event_type = Game.LAST_EFFECT
			elif delta_category == AssetDelta.EFFECT_CRASH:
				event_type = Game.CRASH_EFFECT
			else:
				raise Exception("Unknown category of effect : %s" % (delta_category))

			self.game.add_event(event_type=event_type, data={"triggered_corporation": self.base_corporation.name, "delta": delta, "abs_delta": abs(delta), "market": corporation_market.market.name, "corporation": corporation.base_corporation.name}, delta=delta, corporation=corporation, corporation_market=corporation_market)

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

	def update_modifier(self, delta=0):
		"""
		Updates assets_modifier value, in/decreasing it by given delta and saves the model
		Must be used for all modifications on assets_modifier, because it enforces assets = market_assets + asset_modifier
		"""
		self.assets_modifier += delta
		self.assets = self.market_assets + self.assets_modifier
		self.save()

	def set_market_assets(self, value=0):
		"""
		This is here to replace the assignments 'c.market_assets = xxx', because they do not enforce assets = market_assets + asset_modifier
		**This function should only be used in tests.**
		"""
		self.market_assets = value
		self.assets = self.market_assets + self.assets_modifier
		self.save()

	def increase_market_assets(self, value=1):
		"""
		Increase corporation's market_assets by value
		"""
		self.market_assets += value
		self.assets = self.market_assets + self.assets_modifier
		self.save()

	def update_assets(self, delta, category, corporation_market):
		"""
		Updates market assets values, and saves the model
		Does not actually change "assets", but changes on market_assets will be reflected on assets via increase_market_assets
		"""
		turn = self.game.current_turn
		corporation_market.value += delta
		corporation_market.save()

		# Mirror changes on market assets
		self.increase_market_assets(delta)

		# And register assetdelta for logging purposes
		self.assetdelta_set.create(category=category, delta=delta, turn=turn)

	def __unicode__(self):
		return u"%s (%s)" % (self.base_corporation.name, self.assets)


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
	BUBBLE = 'market*bubble'
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
		(BUBBLE, 'Domination/Perte sèche'),
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
