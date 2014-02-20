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
		'newsfeed': u"Un vol de données à été effectué sur %s",
		'citizens': u"Un vol de données à été effectué sur %s pour le compte de %s",
	},
	'fail': {
		'sponsor': u"Votre équipe a échoué lors de la tentative de DataSteal sur %s pour %s",
		'newsfeed': u"Une tentative de vol de données à été effectué sur %s",
		'citizens': u"Une tentative de vol de données à été effectué sur %s pour le compte de %s",
	},
}

sabotage_messages = {
	'success': {
		'sponsor': u"Votre équipe a réussi à saboter les opérations de %s",
		'newsfeed': u"Un sabotage à été effectué sur %s",
		'citizens': u"Un sabotage à été effectué sur %s",
	},
	'fail': {
		'sponsor': u"Votre équipe a échoué lors de la tentative de DataSteal sur %s",
		'newsfeed': u"Une tentative de sabotage à été effectué sur %s",
		'citizens': u"Une tentative de sabotage à été effectué sur %s",
	},
}

extraction_messages = {
	'success': {
		'sponsor': u"Votre équipe a extraire un scientifique de %s pour le compte de %s",
		'newsfeed': u"Une extraction à été effectué sur %s",
		'citizens': u"Une extraction à été effectué sur %s pour le compte de %s",
	},
	'fail': {
		'sponsor': u"Votre équipe a échoué lors de la tentative d'Extraction sur %s pour %s",
		'newsfeed': u"Une tentative d'extraction à été effectué sur %s",
		'citizens': u"Une tentative d'extraction à été effectué sur %s pour le compte de %s",
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
		for protection in self.get_protection_values():
			if randint(1, 100) <= protection:
				return True
		return False

	def is_detected(self):
		if randint(1, 100) <= self.target_corporation.base_corporation.detection:
			return True
		return False

	def get_protection_values(self):
		values = []
		for protector in self.target_corporation.protectors.filter(defense=self.TYPE):
			values.append(protector.get_success_probability())
		values.append(getattr(self.target_corporation.base_corporation, self.TYPE))
		return values

	def resolve(self):
			self.player.money -= self.get_cost()
			self.player.save()
			if self.is_successful() and not self.is_protected():
				self.resolve_success(self.is_detected())
			else:
				self.resolve_fail(self.is_detected())
				# Repay the player
				self.repay()

	def resolve_successful(self):
		"""
		This function is called when the run has succeeded
		"""
		self.resolve_success(self.is_protected())

	def resolve_failure(self):
		"""
		This function is called when the run has failed.
		"""
		self.resolve_fail(self.is_protected())

	def get_form(self, datas=None):
		form = super(OffensiveRunOrder, self).get_form(datas)
		form.fields['target_corporation'].queryset = self.player.game.corporation_set.all()

		return form


class DataStealOrder(OffensiveRunOrder):
	"""
	Model for DataSteal Runs
	"""
	PROBA_SUCCESS = 30
	TYPE = "datasteal"

	title = "Lancer une run de Datasteal"
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = self.PROBA_SUCCESS
		if self.has_influence_bonus:
			proba += self.INFLUENCE_BONUS
		proba += self.additional_percents * 10
		proba += self.hidden_percents * 10
		return proba

	def resolve_success(self, detected):
		self.stealer_corporation.assets += 1
		self.stealer_corporation.save()

		# Send a note to the one who ordered the DataSteal
		category = u"Run de Datasteal"
		content = datasteal_messages['success']['sponsor'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			category = u"matrix-buzz"
			content = datasteal_messages['success']['citizens'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
			n = Note(
				category=category,
				content=content,
				turn=self.player.game.current_turn,
			)
			n.save()
			n.recipient_set = Player.objects.filter(citizenship__corporation=self.target_corporation)
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
			category = u"matrix-buzz"
			content = datasteal_messages['fail']['citizens'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
			n = Note(
				category=category,
				content=content,
				turn=self.player.game.current_turn,
			)
			n.save()
			n.recipient_set = Player.objects.filter(citizenship__corporation=self.target_corporation)
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
		category = u"matrix-buzz"
		content = sabotage_messages['success']['citizens'] % (self.target_corporation.base_corporation.name)
		n = Note(
				category=category,
				content=content,
				turn=self.player.game.current_turn,
			)
		n.save()
		n.recipient_set = Player.objects.filter(citizenship__corporation=self.target_corporation)
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
			category = u"matrix-buzz"
			content = sabotage_messages['success']['citizens'] % (self.target_corporation.base_corporation.name)
			n = Note(
				category=category,
				content=content,
				turn=self.player.game.current_turn,
			)
			n.save()
			n.recipient_set = Player.objects.filter(citizenship__corporation=self.target_corporation)

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
			category = u"matrix-buzz"
			content = extraction_messages['success']['citizens'] % (self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name)
			n = Note(
				category=category,
				content=content,
				turn=self.player.game.current_turn,
			)
			n.save()
			n.recipient_set = Player.objects.filter(citizenship__corporation=self.target_corporation)
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
			category = u"matrix-buzz"
			content = extraction_messages['fail']['citizens'] % (self.target_corporation.base_corporation.name, self.kidnapper_corporation.base_corporation.name)
			n = Note(
				category=category,
				content=content,
				turn=self.player.game.current_turn,
			)
			n.save()
			n.recipient_set = Player.objects.filter(citizenship__corporation=self.target_corporation)
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

	DEFENSE_CHOICES = (
		(EXTRACTION, "extraction"),
		(DATASTEAL, "datasteal"),
		(SABOTAGE, "sabotage")
	)
	defense = models.CharField(max_length=2, choices=DEFENSE_CHOICES)
	protected_corporation = models.ForeignKey(Corporation, related_name="protectors")

	def clean(self):
		super(ProtectionOrder, self).clean()
		if self.additional_percents > 5:
			raise ValidationError

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 50%
		"""
		proba = 0
		if self.has_influence_bonus:
			proba += self.INFLUENCE_BONUS
		proba += self.additional_percents * 10
		proba += self.hidden_percents * 10
		return proba

	def description(self):
		return u"Envoyer une équipe protéger les intérêts de %s" % (self.protected_corporation.base_corporation.name)

	def get_form(self, datas=None):
		form = super(ProtectionOrder, self).get_form(datas)
		form.fields['protected_corporation'].queryset = self.player.game.corporation_set.all()

		return form


orders = (DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder)
