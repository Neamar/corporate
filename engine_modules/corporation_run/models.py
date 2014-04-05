# -*- coding: utf-8 -*-
from django.db import models
from random import randint
from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation
from messaging.models import Note
from engine.models import Player
from website.widgets import PlainTextField


datasteal_messages = {
	'success': {
		'sponsor': u"Votre équipe a *réussi* un **datasteal** de %s pour le compte de %s",
		'newsfeed': u"Un **datasteal** a *réussi* sur %s",
		'citizens': u"Un **datasteal**, commandité par %s, a *réussi* sur %s pour le compte de %s avec %s%% chances de réussite",
	},
	'fail': {
		'sponsor': u"Votre équipe a *échoué* son **datasteal** sur %s pour %s",
		'newsfeed': u"Un **datasteal** a *échoué* sur %s",
		'citizens': u"Un **datasteal**, commandité par %s, a *échoué* sur %s pour le compte de %s avec %s%% chances de réussite",
	},
}

sabotage_messages = {
	'success': {
		'sponsor': u"Votre équipe a *réussi* un **sabotage** sur les opérations de %s",
		'newsfeed': u"Un **sabotage** a *réussi* sur %s",
		'citizens': u"Un **sabotage**, commandité par %s, a *réussi* sur %s avec %s%% chances de réussite",
	},
	'fail': {
		'sponsor': u"Votre équipe a *échoué* son **sabotage** sur %s",
		'newsfeed': u"Un **sabotage** a *échoué* sur %s",
		'citizens': u"Un **sabotage**, commandité par %s, à *échoué* sur %s avec %s%% chances de réussite",
	},
}

extraction_messages = {
	'success': {
		'sponsor': u"Votre équipe a *réussi* une **extraction** de %s pour le compte de %s",
		'newsfeed': u"Une **extraction** a *réussi* sur %s",
		'citizens': u"Une **extraction**, commanditée par %s, a *réussi* sur %s pour le compte de %s avec %s%% chances de réussite",
	},
	'fail': {
		'sponsor': u"Votre équipe a *échoué* son **extraction** sur %s pour %s",
		'newsfeed': u"Une **extraction** a *échoué* sur %s",
		'citizens': u"Une **extraction**, commanditée par %s, a *échoué* sur %s pour le compte de %s avec %s%% chances de réussite",
	},
}


class OffensiveRunOrder(RunOrder):
	"""
	Model for offensive runs.

	Require subclass to define a property target_corporation, whose values will be used for protection and defense.
	Require constants to be defined:

	* PROTECTION_TYPE : Will be used to find protection run and base default values.
	* TIMING_MALUS_SIMILAR value to consider for the timing malus.
	* BASE_SUCCESS_PROBABILITY base probability for resolution

	Checks for Protection Runs.
	Implements timing malus.
	"""
	class Meta:
		abstract = True

	def is_protected(self):
		"""
		Return True if the run is defended against
		"""
		for protection in self.get_protection_values():
			if randint(1, 100) <= protection:
				return True
		return False

	def is_detected(self):
		"""
		Rturn True if the run is detected
		"""
		if self.target_corporation is None:
			return False

		if randint(1, 100) <= self.target_corporation.base_corporation.detection:
			return True
		return False

	def get_protection_values(self):
		"""
		Return a list of defenses probabilities
		"""
		values = []
		if self.target_corporation is not None:
			for protector in self.target_corporation.protectors.filter(defense=self.PROTECTION_TYPE):
				values.append(protector.get_success_probability())

			values.append(getattr(self.target_corporation.base_corporation, self.PROTECTION_TYPE))
		return values

	def get_raw_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = super(OffensiveRunOrder, self).get_success_probability()
		proba += self.BASE_SUCCESS_PROBABILITY
		return proba

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%. Add timing malus.
		"""
		raw_proba = self.get_raw_probability()

		kwargs = {
			self.TIMING_MALUS_SIMILAR: getattr(self, self.TIMING_MALUS_SIMILAR),
			"turn": self.player.game.current_turn
		}
		similar_runs = self.__class__.objects.filter(**kwargs).exclude(pk=self.pk)
		better_runs = [run for run in similar_runs if run.get_raw_probability() >= raw_proba]
		proba = raw_proba - 10 * len(better_runs)
		return proba

	def resolve(self):
			self.player.money -= self.get_cost()
			self.player.save()
			if self.is_successful() and not self.is_protected():
				self.resolve_success(self.is_detected())
			else:
				self.resolve_fail(self.is_detected())
				# Repay the player
				self.repay()

	def notify_citizens(self, content):
		"""
		Send a message to target_corporation citizens
		"""
		category = u"matrix-buzz"
		n = Note(
			category=category,
			content=content,
			turn=self.player.game.current_turn,
		)
		n.save()
		n.recipient_set = Player.objects.filter(citizenship__corporation=self.target_corporation)


class OffensiveCorporationRunOrder(OffensiveRunOrder):
	"""
	Model for offensive corporation runs.
	"""
	TIMING_MALUS_SIMILAR = 'target_corporation'

	target_corporation = models.ForeignKey(Corporation, related_name="scoundrels")

	def get_form(self, datas=None):
		form = super(OffensiveRunOrder, self).get_form(datas)
		form.fields['target_corporation'].queryset = self.player.game.corporation_set.all()
		form.fields['base_percents'] = PlainTextField(initial="%s%%" % self.BASE_SUCCESS_PROBABILITY)

		return form


class DataStealOrder(OffensiveCorporationRunOrder):
	"""
	Order for DataSteal runs
	"""
	BASE_SUCCESS_PROBABILITY = 30
	PROTECTION_TYPE = "datasteal"

	title = "Lancer une run de Datasteal"
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve_success(self, detected):
		self.stealer_corporation.update_assets(+1)

		# Send a note to the one who ordered the DataSteal
		category = u"Run de Datasteal"
		content = datasteal_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = datasteal_messages['success']['citizens'] % (self.player, self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name, self.get_raw_probability())
			self.notify_citizens(content)
			# Send a note to everybody
			category = u"matrix-buzz"
			path = u'datasteal/%s/success' % self.target_corporation.base_corporation.slug
			self.player.game.add_newsfeed_from_template(category=category, path=path)

	def resolve_fail(self, detected):
		# Send a note to the one who ordered the DataSteal
		category = u"Run de Datasteal"
		content = datasteal_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = datasteal_messages['fail']['citizens'] % (self.player, self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name, self.get_raw_probability())
			self.notify_citizens(content)

			# Send a note to everybody
			category = u"matrix-buzz"
			path = u'datasteal/%s/failure' % self.target_corporation.base_corporation.slug
			self.player.game.add_newsfeed_from_template(category=category, path=path)

	def description(self):
		return u"Envoyer une équipe voler des données de %s pour le compte de %s (%s%%)" % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name, self.get_raw_probability())

	def get_form(self, datas=None):
		form = super(DataStealOrder, self).get_form(datas)
		form.fields['stealer_corporation'].queryset = self.player.game.corporation_set.all()

		return form


class SabotageOrder(OffensiveCorporationRunOrder):
	"""
	Order for Sabotage runs
	"""
	title = "Lancer une run de Sabotage"

	BASE_SUCCESS_PROBABILITY = 30
	PROTECTION_TYPE = "sabotage"

	def resolve_success(self, detected):
		self.target_corporation.update_assets(-2)

		# Send a note to the one who ordered the Sabotage
		category = u"Run de Sabotage"
		content = sabotage_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = sabotage_messages['success']['citizens'] % (self.player, self.target_corporation.base_corporation.name, self.get_raw_probability())
			self.notify_citizens(content)

		# Send a note to everybody
		category = u"matrix-buzz"
		path = u'sabotage/%s/success' % self.target_corporation.base_corporation.slug 
		self.player.game.add_newsfeed_from_template(category=category, path=path)

	def resolve_fail(self, detected):
		# Send a note to the one who ordered the Sabotage
		category = u"Run de Sabotage"
		content = sabotage_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = sabotage_messages['fail']['citizens'] % (self.player, self.target_corporation.base_corporation.name, self.get_raw_probability())
			self.notify_citizens(content)

			# Send a note to everybody
			category = u"matrix-buzz"
			path = u'sabotage/%s/failure' % self.target_corporation.base_corporation.slug
			self.player.game.add_newsfeed_from_template(category=category, path=path)

	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s (%s%%)" % (self.target_corporation.base_corporation.name, self.get_raw_probability())


class ExtractionOrder(OffensiveCorporationRunOrder):
	"""
	Order for Extraction runs
	"""
	title = "Lancer une run d'Extraction"

	BASE_SUCCESS_PROBABILITY = 10
	PROTECTION_TYPE = "extraction"

	kidnapper_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve_success(self, detected):
		self.target_corporation.update_assets(-1)
		self.kidnapper_corporation.update_assets(1)

		# Send a note to the one who ordered the Extraction
		category = u"Run d'Extraction"
		content = extraction_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = extraction_messages['success']['citizens'] % (self.player, self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name, self.get_raw_probability())
			self.notify_citizens(content)

			# Send a note to everybody
			category = u"matrix-buzz"
			path = u'extraction/%s/success' % self.target_corporation.base_corporation.slug
			self.player.game.add_newsfeed_from_template(category=category, path=path)

	def resolve_fail(self, detected):
		# Send a note to the one who ordered the DataSteal
		category = u"Run d'Extraction"
		content = extraction_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = extraction_messages['fail']['citizens'] % (self.player, self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name, self.get_raw_probability())
			self.notify_citizens(content)

			# Send a note to everybody
			category = u"matrix-buzz"
			path = u'extraction/%s/failure' % self.target_corporation.base_corporation.slug
			self.player.game.add_newsfeed_from_template(category=category, path=path)

	def description(self):
		return u"Réaliser une extraction de %s vers %s (%s%%)" % (self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name, self.get_raw_probability())


class ProtectionOrder(RunOrder):
	"""
	Order for Protection runs
	"""
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
	protected_corporation = models.ForeignKey(Corporation, related_name="protectors")

	def get_success_probability(self):
		"""
		Compute success probability, adding base values
		"""
		proba = super(ProtectionOrder, self).get_success_probability()
		proba += self.BASE_SUCCESS_PROBABILITY[self.defense]
		return proba

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()

	def description(self):
		return u"Envoyer une équipe protéger les intérêts de %s (%s%%)" % (self.protected_corporation.base_corporation.name, self.get_success_probability())

	def get_form(self, datas=None):
		form = super(ProtectionOrder, self).get_form(datas)
		form.fields['protected_corporation'].queryset = self.player.game.corporation_set.all()
		form.fields['base_extraction_percents'] = PlainTextField(initial="%s%%" % self.PROBA_EXTRACTION_SUCCESS)
		form.fields['base_datasteal_percents'] = PlainTextField(initial="%s%%" % self.PROBA_DATASTEAL_SUCCESS)
		form.fields['base_sabotage_percents'] = PlainTextField(initial="%s%%" % self.PROBA_SABOTAGE_SUCCESS)

		return form


orders = (DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder)
