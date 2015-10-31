# -*- coding: utf-8 -*-
from django.db import models
from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation, AssetDelta
from website.widgets import PlainTextField
from engine_modules.market.models import CorporationMarket
from engine.models import Game


class CorporationRunOrder(RunOrder):
	"""
	Model for offensive corporation runs.
	"""

	target_corporation_market = models.ForeignKey(CorporationMarket, related_name="scoundrels")

	def get_success_probability(self):
		"""
		Compute success probability, eventually modified by protection runs
		"""
		base_value = super(CorporationRunOrder, self).get_success_probability()

		protection = self.target_corporation_market.protectors.filter(
			turn=self.turn
		)
		if protection.exists():
			return min(base_value, ProtectionOrder.MAX_PERCENTS)
		return base_value

	@property
	def target_corporation(self):
		"""
		Helper function to directly retrieve the corporation from its market
		"""
		return self.target_corporation_market.corporation

	def get_form(self, data=None):
		form = super(CorporationRunOrder, self).get_form(data)
		# We get all the corporationMarket of uncrashed corporations
		form.fields['target_corporation_market'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game, corporation__crash_turn__isnull=True, turn=self.player.game.current_turn)
		form.fields['base_percents'] = PlainTextField(initial="%s%%" % self.BASE_SUCCESS_PROBABILITY)

		return form


class CorporationRunOrderWithStealer(CorporationRunOrder):
	"""
	Offensive run with a stealer (e.g. DataStealOrder / ExtractionOrder)
	"""
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")

	@property
	def stealer_corporation_market(self):
		"""
		Helper function to directly retrieve the market for the stealer
		"""
		return self.stealer_corporation.corporationmarket_set.get(market=self.target_corporation_market.market_id, turn=self.player.game.current_turn)

	def get_form(self, data=None):
		form = super(CorporationRunOrderWithStealer, self).get_form(data)
		form.fields['stealer_corporation'].queryset = self.player.game.corporation_set.all()

		return form


class DataStealOrder(CorporationRunOrderWithStealer):
	"""
	Order for DataSteal runs
	"""
	ORDER = 500

	title = "Lancer une run de Datasteal"

	def resolve_successful(self):
		self.stealer_corporation.update_assets(+1, corporation_market=self.stealer_corporation_market, category=AssetDelta.RUN_DATASTEAL)

		# create a game_event on the stealer
		self.player.game.add_event(event_type=Game.OPE_DATASTEAL_UP, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, delta=1, corporation=self.stealer_corporation, corporation_market=self.stealer_corporation_market, players=[self.player])
		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_DATASTEAL_DOWN, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def resolve_failure(self):
		# create a game_event on the stealer
		self.player.game.add_event(event_type=Game.OPE_DATASTEAL_FAIL_UP, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.stealer_corporation, corporation_market=self.stealer_corporation_market, players=[self.player])
		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_DATASTEAL_FAIL_DOWN, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def description(self):
		return u"Envoyer une équipe voler des données de %s (%s) pour le compte de %s (%s%%)" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.stealer_corporation.base_corporation.name, self.get_raw_probability())


class ExtractionOrder(CorporationRunOrderWithStealer):
	"""
	Order for Extraction runs
	"""
	ORDER = 700
	title = "Lancer une run d'Extraction"

	def resolve_successful(self):
		self.target_corporation.update_assets(-1, corporation_market=self.target_corporation_market, category=AssetDelta.RUN_EXTRACTION)
		self.stealer_corporation.update_assets(1, corporation_market=self.stealer_corporation_market, category=AssetDelta.RUN_EXTRACTION)

		# create a game_event on the stealer
		self.player.game.add_event(event_type=Game.OPE_EXTRACTION_UP, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, delta=1, corporation=self.stealer_corporation, corporation_market=self.stealer_corporation_market, players=[self.player])
		# create a game_event on the target
		self.player.game.add_event(event_type=Game.OPE_EXTRACTION_DOWN, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, delta=-1, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def resolve_failure(self):
		# create a game_event on the stealer
		self.player.game.add_event(event_type=Game.OPE_EXTRACTION_FAIL_UP, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.stealer_corporation, corporation_market=self.stealer_corporation_market, players=[self.player])
		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_EXTRACTION_FAIL_DOWN, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def description(self):
		return u"Réaliser une extraction de %s (%s) vers %s (%s%%)" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.stealer_corporation.base_corporation.name, self.get_raw_probability())


class SabotageOrder(CorporationRunOrder):
	"""
	Order for Sabotage runs
	"""
	ORDER = 600
	title = "Lancer une run de Sabotage"

	def resolve_successful(self):
		self.target_corporation.update_assets(-2, corporation_market=self.target_corporation_market, category=AssetDelta.RUN_SABOTAGE)

		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_SABOTAGE, delta=-2, data={"player": self.player.name, "market": self.target_corporation_market.market.name, "corporation": self.target_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def resolve_failure(self):
		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_SABOTAGE_FAIL, data={"player": self.player.name, "market": self.target_corporation_market.market.name, "corporation": self.target_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s (%s) (%s%%)" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.get_raw_probability())

	def get_form(self, data=None):
		form = super(SabotageOrder, self).get_form(data)
		# we can't make a sabotage on a negative or null corporationMarket
		form.fields['target_corporation_market'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game, corporation__crash_turn__isnull=True, turn=self.player.game.current_turn, value__gt=0)

		return form


class ProtectionOrder(RunOrder):
	"""
	Order for Protection runs
	"""
	ORDER = 850
	title = "Lancer une run de Protection"
	MAX_PERCENTS = 40

	protected_corporation_market = models.ForeignKey(CorporationMarket, related_name="protectors")

	@property
	def protected_corporation(self):
		"""
		Helper function to directly retrieve the corporation from its market
		"""
		return self.protected_corporation_market.corporation

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()

		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_PROTECTION, data={"player": self.player.name, "market": self.protected_corporation_market.market.name, "corporation": self.protected_corporation.base_corporation.name}, corporation=self.protected_corporation, corporation_market=self.protected_corporation_market, players=[self.player])

	def description(self):
		return u"Envoyer une équipe protéger %s (%s%%)" % (self.protected_corporation.base_corporation.name, self.get_success_probability())

	def get_form(self, data=None):
		form = super(ProtectionOrder, self).get_form(data)
		form.fields['protected_corporation_market'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game, turn=self.player.game.current_turn)

		return form


orders = (DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder)
