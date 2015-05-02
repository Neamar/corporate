# -*- coding: utf-8 -*-
from django.db import models
from engine_modules.run.models import RunOrder
from messaging.models import Newsfeed, Note
from engine_modules.corporation.models import Corporation, AssetDelta
from website.widgets import PlainTextField
from engine_modules.market.models import CorporationMarket
from engine.models import Game


datasteal_messages = {
	'success': {
		'sponsor': u"Votre équipe a *réussi* un **Datasteal** de %s pour le compte de %s",
		'newsfeed': u"Un **Datasteal** a *réussi* sur %s",
		'citizens': u"Un **Datasteal**, commandité par %s, a *réussi* sur %s pour le compte de %s avec %s%% de chances de réussite",
	},
	'fail': {
		'sponsor': u"Votre équipe a *échoué* son **Datasteal** sur %s pour %s",
		'newsfeed': u"Un **Datasteal** a *échoué* sur %s",
		'citizens': u"Un **Datasteal**, commandité par %s, a *échoué* sur %s pour le compte de %s avec %s%% de chances de réussite",
	},
}

sabotage_messages = {
	'success': {
		'sponsor': u"Votre équipe a *réussi* un **Sabotage** sur les opérations de %s",
		'newsfeed': u"Un **Sabotage** a *réussi* sur %s",
		'citizens': u"Un **Sabotage**, commandité par %s, a *réussi* sur %s avec %s%% de chances de réussite",
		'citizens_undetected': u"Un **Sabotage** a *réussi* sur %s.",
	},
	'fail': {
		'sponsor': u"Votre équipe a *échoué* son **Sabotage** sur %s",
		'newsfeed': u"Un **Sabotage** a *échoué* sur %s",
		'citizens': u"Un **Sabotage**, commandité par %s, à *échoué* sur %s avec %s%% de chances de réussite",
	},
}

extraction_messages = {
	'success': {
		'sponsor': u"Votre équipe a *réussi* une **Extraction** de %s pour le compte de %s",
		'newsfeed': u"Une **Extraction** a *réussi* sur %s",
		'citizens': u"Une **Extraction**, commanditée par %s, a *réussi* sur %s pour le compte de %s avec %s%% de chances de réussite",
	},
	'fail': {
		'sponsor': u"Votre équipe a *échoué* son **Extraction** sur %s pour %s",
		'newsfeed': u"Une **Extraction** a *échoué* sur %s",
		'citizens': u"Une **Extraction**, commanditée par %s, a *échoué* sur %s pour le compte de %s avec %s%% de chances de réussite",
	},
}


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
		form.fields['target_corporation_market'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game)
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
		return self.stealer_corporation.corporationmarket_set.get(market=self.target_corporation_market.market_id)

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
		stealer_corporation_market=self.stealer_corporation_market
		self.stealer_corporation.update_assets(+1, corporationmarket=stealer_corporation_market, category=AssetDelta.RUN_DATASTEAL)

		# Send a note to the one who ordered the DataSteal
		content = datasteal_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

		# create a game_event on the stealer
		self.player.game.create_game_event(event_type=Game.OPE_DATASTEAL_UP, data='',  delta=1 , corporation=self.stealer_corporation, corporationmarket=stealer_corporation_market, players=[self.player])
		# create a game event on the target
		self.player.game.create_game_event(event_type=Game.OPE_DATASTEAL_DOWN, data='', corporation=self.target_corporation, corporationmarket=self.target_corporation_market, players=[self.player])

		# And some RP
		path = u'datasteal/%s/success' % self.target_corporation.base_corporation.slug
		self.player.game.add_newsfeed_from_template(category=Newsfeed.MATRIX_BUZZ, path=path)

	def resolve_failure(self):
		# Send a note to the one who ordered the DataSteal
		content = datasteal_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

		# create a game_event on the stealer
		self.player.game.create_game_event(event_type=Game.OPE_DATASTEAL_FAIL_UP, data='', corporation=self.stealer_corporation, corporationmarket=self.stealer_corporation_market, players=[self.player])
		# create a game event on the target
		self.player.game.create_game_event(event_type=Game.OPE_DATASTEAL_FAIL_DOWN, data='', corporation=self.target_corporation, corporationmarket=self.target_corporation_market, players=[self.player])

		# And some RP
		path = u'datasteal/%s/failure' % self.target_corporation.base_corporation.slug
		self.player.game.add_newsfeed_from_template(category=Newsfeed.MATRIX_BUZZ, path=path)

	def description(self):
		return u"Envoyer une équipe voler des données de %s (%s) pour le compte de %s (%s%%)" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.stealer_corporation.base_corporation.name, self.get_raw_probability())


class ExtractionOrder(CorporationRunOrderWithStealer):
	"""
	Order for Extraction runs
	"""
	ORDER = 700
	title = "Lancer une run d'Extraction"

	def resolve_successful(self):
		target_corporation_market=self.target_corporation_market
		stealer_corporation_market=self.stealer_corporation_market
		self.target_corporation.update_assets(-1, corporationmarket=target_corporation_market, category=AssetDelta.RUN_EXTRACTION)
		self.stealer_corporation.update_assets(1, corporationmarket=stealer_corporation_market, category=AssetDelta.RUN_EXTRACTION)

		# Send a note to the one who ordered the Extraction
		content = extraction_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

		# create a game_event on the stealer
		self.player.game.create_game_event(event_type=Game.OPE_EXTRACTION_UP, data='',  delta=1, corporation=self.stealer_corporation, corporationmarket=stealer_corporation_market, players=[self.player])
		# create a game_event on the target
		self.player.game.create_game_event(event_type=Game.OPE_EXTRACTION_DOWN, data='', delta=-1, corporation=self.target_corporation, corporationmarket=target_corporation_market, players=[self.player])

		# Send a note to everybody
		content = extraction_messages['success']['newsfeed'] % (self.target_corporation.base_corporation.name)
		self.player.game.add_newsfeed(category=Newsfeed.MATRIX_BUZZ, content=content)

		# And some RP
		path = u'extraction/%s/success' % self.target_corporation.base_corporation.slug
		self.player.game.add_newsfeed_from_template(category=Newsfeed.MATRIX_BUZZ, path=path)

	def resolve_failure(self):
		# Send a note to the one who ordered the DataSteal
		content = extraction_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

		# create a game_event on the stealer
		self.player.game.create_game_event(event_type=Game.OPE_EXTRACTION_FAIL_UP, data='', corporation=self.stealer_corporation, corporationmarket=self.stealer_corporation_market, players=[self.player])
		# create a game event on the target
		self.player.game.create_game_event(event_type=Game.OPE_EXTRACTION_FAIL_DOWN, data='', corporation=self.target_corporation, corporationmarket=self.target_corporation_market, players=[self.player])

		# Send a note to everybody
		content = extraction_messages['fail']['newsfeed'] % (self.target_corporation.base_corporation.name)
		self.player.game.add_newsfeed(category=Newsfeed.MATRIX_BUZZ, content=content)

		# And some RP
		path = u'extraction/%s/failure' % self.target_corporation.base_corporation.slug
		self.player.game.add_newsfeed_from_template(category=Newsfeed.MATRIX_BUZZ, path=path)

	def description(self):
		return u"Réaliser une extraction de %s (%s) vers %s (%s%%)" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.stealer_corporation.base_corporation.name, self.get_raw_probability())


class SabotageOrder(CorporationRunOrder):
	"""
	Order for Sabotage runs
	"""
	ORDER = 600
	title = "Lancer une run de Sabotage"

	def resolve_successful(self):
		target_corporation_market=self.target_corporation_market
		self.target_corporation.update_assets(-2, corporationmarket=self.target_corporation_market, category=AssetDelta.RUN_SABOTAGE)

		# Send a note to the one who ordered the Sabotage
		content = sabotage_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

		# Send a note to everybody
		content = sabotage_messages['success']['newsfeed'] % (self.target_corporation.base_corporation.name)
		self.player.game.add_newsfeed(category=Newsfeed.MATRIX_BUZZ, content=content)

		# create a game event on the target
		self.player.game.create_game_event(event_type=Game.OPE_SABOTAGE, delta=-2, data='', corporation=self.target_corporation, corporationmarket=target_corporation_market, players=[self.player])

		# And some RP
		path = u'sabotage/%s/success' % self.target_corporation.base_corporation.slug
		self.player.game.add_newsfeed_from_template(category=Newsfeed.MATRIX_BUZZ, path=path)

	def resolve_failure(self):
		# Send a note to the one who ordered the Sabotage
		content = sabotage_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

		# Send a note to everybody
		content = sabotage_messages['fail']['newsfeed'] % (self.target_corporation.base_corporation.name)
		self.player.game.add_newsfeed(category=Newsfeed.MATRIX_BUZZ, content=content)

		# create a game event on the target
		self.player.game.create_game_event(event_type=Game.OPE_SABOTAGE_FAIL, data='', corporation=self.target_corporation, corporationmarket=self.target_corporation_market, players=[self.player])

		# And some RP
		path = u'sabotage/%s/failure' % self.target_corporation.base_corporation.slug
		self.player.game.add_newsfeed_from_template(category=Newsfeed.MATRIX_BUZZ, path=path)

	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s (%s) (%s%%)" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.get_raw_probability())


class ProtectionOrder(RunOrder):
	"""
	Order for Protection runs
	"""
	ORDER = 850
	title = "Lancer une run de Protection"
	MAX_PERCENTS = 50

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
		self.player.game.create_game_event(event_type=Game.OPE_PROTECTION, data='', corporation=self.protected_corporation, corporationmarket=self.protected_corporation_market, players=[self.player])


	def description(self):
		return u"Envoyer une équipe protéger %s (%s%%)" % (self.protected_corporation.base_corporation.name, self.get_success_probability())

	def get_form(self, data=None):
		form = super(ProtectionOrder, self).get_form(data)
		form.fields['protected_corporation_market'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game)

		return form


orders = (DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder)
