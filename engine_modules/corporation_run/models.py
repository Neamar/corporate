# -*- coding: utf-8 -*-
from django.db import models
from random import randint
from django.core.exceptions import ValidationError
from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation
from messaging.models import Note
from engine.models import Player

datasteal_messages = {
	'success': {
		'sponsor': u"Votre équipe a réussi à voler des données de %s pour le compte de %s",
		'newsfeed': u"Un vol de données a été effectué sur %s",
		'citizens': u"Un vol de données a été effectué sur %s pour le compte de %s",
	},
	'fail': {
		'sponsor': u"Votre équipe a échoué lors de la tentative de DataSteal sur %s pour %s",
		'newsfeed': u"Une tentative de vol de données a été effectuée sur %s",
		'citizens': u"Une tentative de vol de données a été effectuée sur %s pour le compte de %s",
	},
}

sabotage_messages = {
	'success': {
		'sponsor': u"Votre équipe a réussi à saboter les opérations de %s",
		'newsfeed': u"Un sabotage a été effectué sur %s",
		'citizens': u"Un sabotage a été effectué sur %s",
	},
	'fail': {
		'sponsor': u"Votre équipe a échoué lors de la tentative de DataSteal sur %s",
		'newsfeed': u"Une tentative de sabotage à été effectuée sur %s",
		'citizens': u"Une tentative de sabotage à été effectuée sur %s",
	},
}

extraction_messages = {
	'success': {
		'sponsor': u"Votre équipe a extrait un scientifique de %s pour le compte de %s",
		'newsfeed': u"Une extraction a été effectuée sur %s",
		'citizens': u"Une extraction a été effectuée sur %s pour le compte de %s",
	},
	'fail': {
		'sponsor': u"Votre équipe a échoué lors de la tentative d'Extraction sur %s pour %s",
		'newsfeed': u"Une tentative d'extraction a été effectuée sur %s",
		'citizens': u"Une tentative d'extraction a été effectuée sur %s pour le compte de %s",
	},
}


class OffensiveRunOrder(RunOrder):
	"""
	Model for offensive corporation runs.

	Implements the check for Protection Runs.

	Exposes 4 functions to override:
	* resolve_success: run ok, protection fail
	* resolve_fail: run fail, protection fail
	* resolve_interception: run ok, protection ok
	* resolve_capture: run fail, protection ok
	"""

	target_corporation = models.ForeignKey(Corporation, related_name="scoundrels")

	def is_protected(self):
		"""
		Return True if the corporation is defended
		"""
		for protection in self.get_protection_values():
			if randint(1, 100) <= protection:
				return True
		return False

	def is_detected(self):
		"""
		Rturn True if the run is detected
		"""
		if randint(1, 100) <= self.target_corporation.base_corporation.detection:
			return True
		return False

	def get_protection_values(self):
		"""
		Return a list of defenses probabilities
		"""
		values = []
		for protector in self.target_corporation.protectors.filter(defense=self.TYPE):
			values.append(protector.get_success_probability())
		values.append(getattr(self.target_corporation.base_corporation, self.TYPE))
		return values

	def get_raw_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = super(OffensiveRunOrder, self).get_success_probability()
		proba += self.PROBA_SUCCESS
		return proba

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%. Add timing malus.
		"""
		raw_proba = self.get_raw_probability()
		similar_runs = self.__class__.objects.filter(target_corporation=self.target_corporation).exclude(pk=self.pk)
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

	def get_form(self, datas=None):
		form = super(OffensiveRunOrder, self).get_form(datas)
		form.fields['target_corporation'].queryset = self.player.game.corporation_set.all()

		return form

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


class DataStealOrder(OffensiveRunOrder):
	"""
	Model for DataSteal Runs
	"""
	PROBA_SUCCESS = 30
	TYPE = "datasteal"

	title = "Lancer une run de Datasteal"
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve_success(self, detected):
		self.stealer_corporation.assets += 1
		self.stealer_corporation.save()

		# Send a note to the one who ordered the DataSteal
		category = u"Run de Datasteal"
		content = datasteal_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = datasteal_messages['success']['citizens'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
			self.notify_citizens(content)
			# Send a note to everybody
			category = u"matrix-buzz"
			content = datasteal_messages['success']['newsfeed'] % (self.target_corporation.base_corporation.name)
			self.player.game.add_newsfeed(category=category, content=content)

	def resolve_fail(self, detected):
		# Send a note to the one who ordered the DataSteal
		category = u"Run de Datasteal"
		content = datasteal_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = datasteal_messages['fail']['citizens'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
			self.notify_citizens(content)

			# Send a note to everybody
			category = u"matrix-buzz"
			content = datasteal_messages['fail']['newsfeed'] % (self.target_corporation.base_corporation.name)
			self.player.game.add_newsfeed(category=category, content=content)

	def description(self):
		return u"Envoyer une équipe voler des données de %s pour le compte de %s" % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)

	def get_form(self, datas=None):
		form = super(DataStealOrder, self).get_form(datas)
		form.fields['stealer_corporation'].queryset = self.player.game.corporation_set.all()

		return form


class SabotageOrder(OffensiveRunOrder):
	"""
	Model for Sabotage Runs
	"""
	title = "Lancer une run de Sabotage"

	PROBA_SUCCESS = 30
	TYPE = "sabotage"

	def resolve_success(self, detected):
		self.target_corporation.assets -= 2
		self.target_corporation.save()

		# Send a note to the one who ordered the Sabotage
		category = u"Run de Sabotage"
		content = sabotage_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to citizens
		content = sabotage_messages['success']['citizens'] % (self.target_corporation.base_corporation.name)
		self.notify_citizens(content)

		# Send a note to everybody
		category = u"matrix-buzz"
		content = sabotage_messages['success']['newsfeed'] % (self.target_corporation.base_corporation.name)
		self.player.game.add_newsfeed(category=category, content=content)

	def resolve_fail(self, detected):
		# Send a note to the one who ordered the Sabotage
		category = u"Run de Sabotage"
		content = sabotage_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = sabotage_messages['success']['citizens'] % (self.target_corporation.base_corporation.name)
			self.notify_citizens(content)

	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s" % (self.target_corporation.base_corporation.name)


class ExtractionOrder(OffensiveRunOrder):
	"""
	Model for Extraction Runs
	"""

	PROBA_SUCCESS = 10
	TYPE = "extraction"

	kidnapper_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve_success(self, detected):
		self.target_corporation.assets -= 1
		self.target_corporation.save()

		self.kidnapper_corporation.assets += 1
		self.kidnapper_corporation.save()

		# Send a note to the one who ordered the Extraction
		category = u"Run d'Extraction"
		content = extraction_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = extraction_messages['success']['citizens'] % (self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name)
			self.notify_citizens(content)

			# Send a note to everybody
			category = u"matrix-buzz"
			content = extraction_messages['success']['newsfeed'] % (self.target_corporation.base_corporation.name)
			self.player.game.add_newsfeed(category=category, content=content)

	def resolve_fail(self, detected):
		# Send a note to the one who ordered the DataSteal
		category = u"Run d'Extraction'"
		content = extraction_messages['fail']['sponsor'] % (self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = extraction_messages['fail']['citizens'] % (self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name)
			self.notify_citizens(content)

			# Send a note to everybody
			category = u"matrix-buzz"
			content = extraction_messages['fail']['newsfeed'] % (self.target_corporation.base_corporation.name)
			self.player.game.add_newsfeed(category=category, content=content)

	def description(self):
		return u"Envoyer une équipe kidnapper un scientifique renommé de %s" % (self.target_corporation.base_corporation.name)


class ProtectionOrder(RunOrder):
	"""
	Model for Protection Runs
	"""
	title = "Lancer une run de Protection"

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

	PROBA_SUCCESS = {
		EXTRACTION: PROBA_EXTRACTION_SUCCESS,
		DATASTEAL: PROBA_DATASTEAL_SUCCESS,
		SABOTAGE: PROBA_SABOTAGE_SUCCESS,
	}

	defense = models.CharField(max_length=2, choices=DEFENSE_CHOICES)
	protected_corporation = models.ForeignKey(Corporation, related_name="protectors")

	def get_success_probability(self):
		"""
		Compute success probability, adding base values
		"""
		proba = super(ProtectionOrder, self).get_success_probability()
		proba += self.PROBA_SUCCESS[self.defense]
		return proba

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()

	def description(self):
		return u"Envoyer une équipe protéger les intérêts de %s" % (self.protected_corporation.base_corporation.name)

	def get_form(self, datas=None):
		form = super(ProtectionOrder, self).get_form(datas)
		form.fields['protected_corporation'].queryset = self.player.game.corporation_set.all()

		return form


orders = (DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder)
