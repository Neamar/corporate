# -*- coding: utf-8 -*-
from django.db import models
from random import randint
from django.core.exceptions import ValidationError
from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation

datasteal_messages = {
	'success': u"Votre équipe a réussi à voler des données de %s pour le compte de %s",
	'fail': u"Votre équipe a échoué lors de la tentative de DataSteal sur %s pour %s",
	'interception': {
		'aggressor': u"Votre équipe a été interceptée lors de la tentative de DataSteal sur %s. Elle a cependant réussi à s'enfuir",
		'protector': u"Votre équipe a réussi à protéger %s d'une tentative de DataSteal. L'équipe adverse a cependant réussi à s'enfuir",
	},
	'capture': {
		'aggressor': u"Votre équipe a été capturée par une autre lors de la tentative de DataSteal sur %s. Le commanditaire est au courant de vos agissements",
			'protector'	: u"Votre équipe a réussi à capturer une équipe de %s lors d'une tentative de DataSteal sur %s pour le compte de %s.",
	}
}

sabotage_messages = {
	'success': u"Votre équipe a réussi à saboter les opérations de %s",
	'fail': u"La tentative de votre équipe pour saboter %s a échoué",
	'interception': {
		'aggressor': u"Votre équipe a été inerceptée par une autre lors de la tentative de Sabotage sur %s. Elle a cependant réussi à s'enfuir",
		'protector': u"Votre équipe a réussi à protéger %s d'une tentative de Sabotage. L'équipe adverse a cependant réussi à s'enfuir",
	},
	'capture': {
		'aggressor': u"L'équipe que vous aviez envoyée saboter %s a été capturée",
		'protector': u"Votre équipe a réussi à capturer une équipe de %s lors d'une tentative de Sabotage sur %s",
	}
}

extraction_messages = {
	'success': u"Votre équipe a réussi à kidnapper un scientifique de %s",
	'fail': u"La tentative de votre équipe pour kidnapper un scientifique %s a échoué",
	'interception': {
		'aggressor': u"Votre équipe a été inerceptée par une autre lors de la tentative d'Extraction' sur %s. Elle a cependant réussi à s'enfuir",
		'protector': u"Votre équipe a réussi à protéger %s d'une tentative d'Extraction'. L'équipe adverse a cependant réussi à s'enfuir",
	},
	'capture': {
		'aggressor': u"L'équipe que vous aviez envoyée kidnapper un scientifique %s a été capturée",
		'protector': u"Votre équipe a réussi à capturer une équipe de %s lors d'une tentative d'Extraction sur %s",
	}
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

	def resolve(self):
		raise NotImplementedError()

	def resolve_successful(self):
		"""

		"""
		raise NotImplementedError()

	def resolve_failure(self):
		"""

		"""
		raise NotImplementedError()

	def resolve_success(self):
		"""
		This method is called when the Offensive Run succeeds on a corporation that has no successful Protection Run.

		It must be overriden
		"""
		raise NotImplementedError()

	def resolve_fail(self):
		"""
		This method is called when the Offensive Run fails on a corporation that has no successful Protection Run.

		It must be overriden
		"""
		raise NotImplementedError()

	def resolve_interception(self, protections):
		"""
		This method is called when the Offensive Run succeeds on a corporation that has a successful Protection Run.

		It must be overriden
		"""
		raise NotImplementedError()

	def resolve_capture(self, protections):
		"""
		This method is called when the Offensive Run fails on a corporation that has a successful Protection Run.

		It must be overriden
		"""
		raise NotImplementedError()

	def get_form(self, datas=None):
		form = super(OffensiveRunOrder, self).get_form(datas)
		form.fields['target_corporation'].queryset = self.player.game.corporation_set.all()

		return form


class DataStealOrder(OffensiveRunOrder):
	"""
	Model for DataSteal Runs
	"""
	PROBA_SUCCESS = 30
	title = "Lancer une run de Datasteal"
	has_succeeded = models.BooleanField(default=False, editable=False)
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()
		protected = False
		for protector in self.target_corporation.protectors.filter(defense=ProtectionOrder.DATASTEAL):
			if protector.protect():
				protected = True
				break

		if self.is_successful():
			if protected or randint(1, 100) <= self.target_corporation.base_corporation.datasteal:
				# succesful attack but defended
				self.resolve_interception(self.target_corporation.protectors.filter(defense=ProtectionOrder.DATASTEAL))
			else:
				# Succesful attack
				self.resolve_success()
		else:
			# Attack failure
			if protected or randint(1, 100) <= self.target_corporation.base_corporation.datasteal:
				# Attack failure and successful defense
				self.resolve_capture(self.target_corporation.protectors.filter(defense=ProtectionOrder.DATASTEAL))
			else:
				# Defense failure too
				self.resolve_fail()

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

	def resolve_success(self):
		self.has_succeeded = True
		self.save()
		self.stealer_corporation.assets += 1
		self.stealer_corporation.save()

		# Send a note for final message
		category = u"Run de Datasteal"
		content = datasteal_messages['success'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

	def resolve_fail(self):
		# Send a note for final message
		category = u"Run de Datasteal"
		content = datasteal_messages['fail'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Repay the player
		self.repay()

	def resolve_interception(self, protections):
		# Send a note to the one who ordered the DataSteal
		category = u"Run de Datasteal"
		content = datasteal_messages['interception']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to protectors
		category = u"Run de Protection"
		content = datasteal_messages['interception']['protector'] % (self.target_corporation.base_corporation.name)
		for protection in protections:
			protection.player.add_note(category=category, content=content)

		# Repay the player
		self.repay()

	def resolve_capture(self, protections):
		# Send a note to the one who ordered the DataSteal
		category = u"Run de Datasteal"
		content = datasteal_messages['capture']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to protectors
		category = u"Run de Protection"
		content = datasteal_messages['capture']['protector'] % (self.player.name, self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		for protection in protections:
			protection.player.add_note(category=category, content=content)

		# Repay the player
		self.repay()

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

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()
		protected = False

		for protector in self.target_corporation.protectors.filter(defense=ProtectionOrder.SABOTAGE):
			if protector.protect():
				protected = True
				break

		if self.is_successful():
			if protected or randint(1, 100) <= self.target_corporation.base_corporation.sabotage:
				# succesful attack but defended
				self.resolve_interception(self.target_corporation.protectors.filter(defense=ProtectionOrder.SABOTAGE))
			else:
				# Succesful attack
				self.resolve_success()
		else:
			# Attack failure
			if protected or randint(1, 100) <= self.target_corporation.base_corporation.sabotage:
				# Attack failure and successful defense
				self.resolve_capture(self.target_corporation.protectors.filter(defense=ProtectionOrder.SABOTAGE))
			else:
				# Defense failure too
				self.resolve_fail()

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = self.PROBA_SUCCESS
		if self.has_influence_bonus:
			proba += 30
		proba += self.additional_percents * 10
		proba += self.hidden_percents * 10
		return proba

	def resolve_success(self):
		self.target_corporation.assets -= 2
		self.target_corporation.save()

		# Send a note for final message
		category = u"Run de Sabotage"
		content = sabotage_messages['success'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

	def resolve_fail(self):
		# Send a note for final message
		category = u"Run de Sabotage"
		content = sabotage_messages['fail'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Repay the player
		self.repay()

	def resolve_interception(self, protections):
		# Send a note to the one who ordered the Sabotage
		category = u"Run de Sabotage"
		content = sabotage_messages['interception']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to protectors
		category = u"Run de Protection"
		content = sabotage_messages['interception']['protector'] % (self.target_corporation.base_corporation.name)
		for protection in protections:
			protection.player.add_note(category=category, content=content)

		# Repay the player
		self.repay()

	def resolve_capture(self, protections):
		# Send a note for final message
		category = u"Run de Sabotage"
		content = sabotage_messages['capture']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to protectors
		category = u"Run de Protection"
		content = sabotage_messages['capture']['protector'] % (self.player, self.target_corporation.base_corporation.name)
		for protection in protections:
			protection.player.add_note(category=category, content=content)

		# Repay the player
		self.repay()

	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s" % (self.target_corporation.base_corporation.name)


class ExtractionOrder(OffensiveRunOrder):
	"""
	Model for Extraction Runs
	"""

	PROBA_SUCCESS = 10

	kidnapper_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()
		protected = False
		for protector in self.target_corporation.protectors.filter(defense=ProtectionOrder.EXTRACTION):
			if protector.protect():
				protected = True
				break

		if self.is_successful():
			if protected or randint(1, 100) <= self.target_corporation.base_corporation.extraction:
				# succesful attack but defended
				self.resolve_interception(self.target_corporation.protectors.filter(defense=ProtectionOrder.EXTRACTION))
			else:
				# Succesful attack
				self.resolve_success()
		else:
			# Attack failure
			if protected or randint(1, 100) <= self.target_corporation.base_corporation.extraction:
				# Attack failure and successful defense
				self.resolve_capture(self.target_corporation.protectors.filter(defense=ProtectionOrder.EXTRACTION))
			else:
				# Defense failure too
				self.resolve_fail()

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = self.PROBA_SUCCESS
		if self.has_influence_bonus:
			proba += 30
		proba += self.additional_percents * 10
		proba += self.hidden_percents * 10
		return proba

	def resolve_success(self):
		self.target_corporation.assets -= 1
		self.target_corporation.save()

		self.kidnapper_corporation.assets += 1
		self.kidnapper_corporation.save()

		# Send a note for final message
		category = u"Run d'Extraction"
		content = extraction_messages['success'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

	def resolve_fail(self):
		# Send a note for final message
		category = u"Run d'Extraction"
		content = extraction_messages['fail'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Repay the player
		self.repay()

	def resolve_interception(self, protections):
		# Send a note to the one who ordered the Extraction
		category = u"Run d'Extraction"
		content = extraction_messages['interception']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to protectors
		category = u"Run de Protection"
		content = extraction_messages['interception']['protector'] % (self.target_corporation.base_corporation.name)
		for protection in protections:
			protection.player.add_note(category=category, content=content)

		# Repay the player
		self.repay()

	def resolve_capture(self, protections):
		# Send a note for final message
		category = u"Run d'Extraction"
		content = extraction_messages['capture']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to protectors
		category = u"Run de Protection"
		content = extraction_messages['capture']['protector'] % (self.player, self.target_corporation.base_corporation.name)
		for protection in protections:
			protection.player.add_note(category=category, content=content)

		# Repay the player
		self.repay()

	def description(self):
		return u"Envoyer une équipe kidnapper un scientifique renommé de %s" % (self.target_corporation.base_corporation.name)


class ProtectionOrder(RunOrder):
	"""
	Model for Protection Runs
	"""
	title = "Lancer une run de Protection"

	EXTRACTION = "ex"
	DATASTEAL = "ds"
	SABOTAGE = "sa"

	DEFENSE_CHOICES = (
		(EXTRACTION, "extraction"),
		(DATASTEAL, "datasteal"),
		(SABOTAGE, "sabotage")
	)
	defense = models.CharField(max_length=2, choices=DEFENSE_CHOICES)
	proba_success = models.PositiveSmallIntegerField()
	protected_corporation = models.ForeignKey(Corporation, related_name="protectors")

	def clean(self):
		super(ProtectionOrder, self).clean()
		self.proba_success = getattr(self.protected_corporation.base_corporation, self.get_defense_display())
		if self.additional_percents > 5:
			raise ValidationError

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 50%
		"""
		proba = self.proba_success
		if self.has_influence_bonus:
			proba += self.INFLUENCE_BONUS
		proba += self.additional_percents * 10
		proba += self.hidden_percents * 10
		return proba

	def protect(self):
		if randint(1, 100) <= self.get_success_probability():
			return True
		return False

	def description(self):
		return u"Envoyer une équipe protéger les intérêts de %s" % (self.protected_corporation.base_corporation.name)

	def get_form(self, datas=None):
		form = super(ProtectionOrder, self).get_form(datas)
		form.fields['protected_corporation'].queryset = self.player.game.corporation_set.all()

		return form


orders = (DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder)
