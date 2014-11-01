# -*- coding: utf-8 -*-
from django.db import models
from random import randint
from engine_modules.run.models import RunOrder
from messaging.models import Newsfeed, Note
from engine_modules.corporation.models import Corporation, AssetDelta
from website.widgets import PlainTextField
from engine_modules.market.models import CorporationMarket


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


class OffensiveCorporationRunOrder(RunOrder):
	"""
	Model for offensive corporation runs.
	"""
	target_corporation_market = models.ForeignKey(CorporationMarket, related_name="scoundrels")

	def get_success_probability(self):
		"""
		Compute success probability, eventually modified by protection runs
		"""
		base_value = super(OffensiveCorporationRunOrder, self).get_success_probability()

		protection = self.target_corporation.protectors.filter(
			target_corporation_market=self.target_corporation_market,
			defense=self.PROTECTION_TYPE,
			turn=self.turn
		)
		if protection.exists():
			return min(base_value, ProtectionOrder.MAX_PERCENTS)
		return base_value

	@property
	def target_corporation(self):
		"""
		Helper function to directly retrieve the corporation
		"""
		return self.target_corporation_market.corporation

	def get_form(self, data=None):
		form = super(OffensiveCorporationRunOrder, self).get_form(data)
		form.fields['target_corporation_market'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game)
		form.fields['base_percents'] = PlainTextField(initial="%s%%" % self.BASE_SUCCESS_PROBABILITY)

		return form


class OffensiveCorporationRunOrderWithStealer(OffensiveCorporationRunOrder):
	"""
	Offensive run with a stealer (e.g. DataStealOrder / ExtractionOrder)
	"""
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")

	@property
	def stealer_corporation_market(self):
		return self.stealer_corporation.corporationmarket_set.get(market=self.target_corporation_market.market_id)

	def get_form(self, data=None):
		form = super(OffensiveCorporationRunOrderWithStealer, self).get_form(data)
		form.fields['stealer_corporation'].queryset = self.player.game.corporation_set.all()

		return form


class DataStealOrder(OffensiveCorporationRunOrderWithStealer):
	"""
	Order for DataSteal runs
	"""
	ORDER = 500
	PROTECTION_TYPE = "datasteal"

	title = "Lancer une run de Datasteal"

	def resolve_successful(self):
		self.stealer_corporation.update_assets(+1, market=self.target_corporation_market.market)

		# Send a note to the one who ordered the DataSteal
		content = datasteal_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

		# And some RP
		path = u'datasteal/%s/success' % self.target_corporation.base_corporation.slug
		self.player.game.add_newsfeed_from_template(category=Newsfeed.MATRIX_BUZZ, path=path)

	def resolve_failure(self):
		# Send a note to the one who ordered the DataSteal
		content = datasteal_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

		# And some RP
		path = u'datasteal/%s/failure' % self.target_corporation.base_corporation.slug
		self.player.game.add_newsfeed_from_template(category=Newsfeed.MATRIX_BUZZ, path=path)

	def description(self):
		return u"Envoyer une équipe voler des données de %s (%s) pour le compte de %s (%s%%)" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.stealer_corporation.base_corporation.name, self.get_raw_probability())


class ExtractionOrder(OffensiveCorporationRunOrderWithStealer):
	"""
	Order for Extraction runs
	"""
	ORDER = 700
	title = "Lancer une run d'Extraction"

	PROTECTION_TYPE = "extraction"

	def resolve_successful(self):
		self.target_corporation.update_assets(-1, market=self.target_corporation_market.market, category=AssetDelta.RUN_EXTRACTION)
		self.stealer_corporation.update_assets(1, market=self.target_corporation_market.market)

		# Send a note to the one who ordered the Extraction
		content = extraction_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

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

		# Send a note to everybody
		content = extraction_messages['fail']['newsfeed'] % (self.target_corporation.base_corporation.name)
		self.player.game.add_newsfeed(category=Newsfeed.MATRIX_BUZZ, content=content)

		# And some RP
		path = u'extraction/%s/failure' % self.target_corporation.base_corporation.slug
		self.player.game.add_newsfeed_from_template(category=Newsfeed.MATRIX_BUZZ, path=path)

	def description(self):
		return u"Réaliser une extraction de %s (%s) vers %s (%s%%)" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.stealer_corporation.base_corporation.name, self.get_raw_probability())


class SabotageOrder(OffensiveCorporationRunOrder):
	"""
	Order for Sabotage runs
	"""
	ORDER = 600
	title = "Lancer une run de Sabotage"

	PROTECTION_TYPE = "sabotage"

	def resolve_successful(self):
		self.target_corporation.update_assets(-2, market=self.target_corporation_market.market, category=AssetDelta.RUN_SABOTAGE)

		# Send a note to the one who ordered the Sabotage
		content = sabotage_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=Note.RUNS, content=content)

		# Send a note to everybody
		content = sabotage_messages['success']['newsfeed'] % (self.target_corporation.base_corporation.name)
		self.player.game.add_newsfeed(category=Newsfeed.MATRIX_BUZZ, content=content)

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

	EXTRACTION = "extraction"
	DATASTEAL = "datasteal"
	SABOTAGE = "sabotage"

	PROBA_DATASTEAL_SUCCESS = 40
	PROBA_EXTRACTION_SUCCESS = 10
	PROBA_SABOTAGE_SUCCESS = 0

	DEFENSE_CHOICES = (
		(EXTRACTION, "Extraction"),
		(DATASTEAL, "Datasteal"),
		(SABOTAGE, "Sabotage")
	)

	BASE_SUCCESS_PROBABILITY = {
		EXTRACTION: PROBA_EXTRACTION_SUCCESS,
		DATASTEAL: PROBA_DATASTEAL_SUCCESS,
		SABOTAGE: PROBA_SABOTAGE_SUCCESS,
	}

	defense = models.CharField(max_length=15, choices=DEFENSE_CHOICES)
	target_corporation_market = models.ForeignKey(CorporationMarket)
	protected_corporation = models.ForeignKey(Corporation, related_name="protectors")

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()

	def description(self):
		return u"Envoyer une équipe protéger %s des %ss (%s%%)" % (self.protected_corporation.base_corporation.name, self.get_defense_display(), self.get_success_probability())

	def get_form(self, data=None):
		form = super(ProtectionOrder, self).get_form(data)
		form.fields['protected_corporation'].queryset = self.player.game.corporation_set.all()
		form.fields['base_extraction_percents'] = PlainTextField(initial="%s%%" % self.PROBA_EXTRACTION_SUCCESS)
		form.fields['base_datasteal_percents'] = PlainTextField(initial="%s%%" % self.PROBA_DATASTEAL_SUCCESS)
		form.fields['base_sabotage_percents'] = PlainTextField(initial="%s%%" % self.PROBA_SABOTAGE_SUCCESS)

		return form


orders = (DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder)
