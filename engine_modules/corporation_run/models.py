# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator
from random import randint

from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation

datasteal_messages = {
	'success': u"Votre équipe a réussi à voler des données de %s pour le compte de %s",
	'fail': u"Votre équipe a échoué lors de la tentative de DataSteal sur %s pour %s",
	'interception'	: {
		'aggressor'	: u"Votre équipe a été interceptée lors de la tentative de DataSteal sur %s. Elle a cependant réussi à s'enfuir",
		'protector'	: u"Votre équipe a réussi à protéger %s d'une tentative de DataSteal. L'équipe adverse a cependant réussi à s'enfuir",
	},
	'capture': {
		'aggressor': u"Votre équipe a été capturée par une autre lors de la tentative de DataSteal sur %s. Le commanditaire est au courant de vos agissements",
			'protector'	: u"Votre équipe a réussi à capturer une équipe de %s lors d'une tentative de DataSteal sur %s pour le compte de %s.",
	},
	'late': u"Votre équipe s'est introduite chez %s mais n'a pas trouvé de donées intéressantes pour %s"
}

sabotage_messages = {
	'success': u"Votre équipe a réussi à saboter les opérations de %s",
	'fail': u"La tentative de votre équipe pour saboter %s a échoué",
	'interception'	: {
		'aggressor'	: u"Votre équipe a été inerceptée par une autre lors de la tentative de Sabotage sur %s. Elle a cependant réussi à s'enfuir",
		'protector'	: u"Votre équipe a réussi à protéger %s d'une tentative de Sabotage. L'équipe adverse a cependant réussi à s'enfuir",
	},
	'capture': {
		'aggressor': u"L'équipe que vous aviez envoyée saboter %s a été capturée",
		'protector'	: u"Votre équipe a réussi à capturer une équipe de %s lors d'une tentative de Sabotage sur %s",
	}
}

extraction_messages = {
	'success': u"Votre équipe a réussi à kidnapper un scientifique de %s",
	'fail': u"La tentative de votre équipe pour kidnapper un scientifique %s a échoué",
	'interception'	: {
		'aggressor'	: u"Votre équipe a été inerceptée par une autre lors de la tentative d'Extraction' sur %s. Elle a cependant réussi à s'enfuir",
		'protector'	: u"Votre équipe a réussi à protéger %s d'une tentative d'Extraction'. L'équipe adverse a cependant réussi à s'enfuir",
	},
	'capture': {
		'aggressor' : u"L'équipe que vous aviez envoyée kidnapper un scientifique %s a été capturée",
		'protector'	: u"Votre équipe a réussi à capturer une équipe de %s lors d'une tentative d'Extraction sur %s",
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

	def resolve_interception(self, po):
		"""
		This method is called when the Offensive Run succeeds on a corporation that has a successful Protection Run.

		It must be overriden
		"""
		raise NotImplementedError()

	def resolve_capture(self, po):
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

		if self.is_successful():
			if self.target_corporation.protectors.filter(done=True).count() >= 1 or randint(1, 100) <= self.target_corporation.datasteal_protection:
				# succesful attack but defended
				self.resolve_interception()
			else:
				# Succesful attack
				self.resolve_success()
		else:
			# Attack failure
			if self.target_corporation.protectors.filter(done=True).count() >= 1 or randint(1, 100) <= self.target_corporation.datasteal_protection:
				# Defense failure too
				self.resolve_fail()
			else:
				# Attack failure and successful defense
				self.resolve_capture

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = self.PROBA_SUCCESS
		if self.has_influence_bonus:
			proba += 30
		proba += self.additional_percents * 10

		return proba

	def resolve_success(self):

		# Get a list of datasteals that have succeeded on this corporation this turn (actually there should be 0 or 1)
		success_datasteals = self.target_corporation.scoundrels.filter(type="DataStealOrder", datastealorder__has_succeeded=True)
		if(success_datasteals.exists()):
			# Send a note for final message
			category = u"Run de Datasteal"
			content = datasteal_messages['late'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
			self.player.add_note(category=category, content=content)
		else:
			self.has_succeeded = True
			self.save()
			self.stealer_corporation.assets += 1
			self.stealer_corporation.save()

			# Send a note for final message
			category = u"Run de Datasteal"
			content = datasteal_messages['success'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
			self.player.add_note(category=category, content=content)
		return True

	def resolve_fail(self):
		# Send a note for final message
		category = u"Run de Datasteal"
		content = datasteal_messages['fail'] % (self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

	def resolve_interception(self, po):
		# Send a note to the one who ordered the DataSteal
		category = u"Run de Datasteal"
		content = datasteal_messages['interception']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to the one who ordered the Protection
		category = u"Run de Protection"
		content = datasteal_messages['interception']['protector'] % (self.target_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)

	def resolve_capture(self, po):
		# Send a note to the one who ordered the DataSteal
		category = u"Run de Datasteal"
		content = datasteal_messages['capture']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to the one who ordered the Protection
		category = u"Run de Protection"
		content = datasteal_messages['capture']['protector'] % (self.player.name, self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)

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

		if self.is_successful():
			if self.target_corporation.protectors.filter(done=True).count() >= 1 or randint(1, 100) <= self.target_corporation.sabotage_protection:
				# succesful attack but defended
				self.resolve_interception()
			else:
				# Succesful attack
				self.resolve_success()
		else:
			# Attack failure
			if self.target_corporation.protectors.filter(done=True).count() >= 1 or randint(1, 100) <= self.target_corporation.sabotage_protection:
				# Defense failure too
				self.resolve_fail()
			else:
				# Attack failure and successful defense
				self.resolve_capture()

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = self.PROBA_SUCCESS
		if self.has_influence_bonus:
			proba += 30
		proba += self.additional_percents * 10

		return proba

	def resolve_success(self):
		self.target_corporation.assets -= 1
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

	def resolve_interception(self, po):
		# Send a note to the one who ordered the DataSteal
		category = u"Run de Sabotage"
		content = sabotage_messages['interception']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to the one who ordered the Protection
		category = u"Run de Protection"
		content = sabotage_messages['interception']['protector'] % (self.target_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)

	def resolve_capture(self, po):
		# Send a note for final message
		category = u"Run de Sabotage"
		content = sabotage_messages['capture']['aggressor'] % (self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to the one who ordered the Protection
		category = u"Run de Protection"
		content = sabotage_messages['capture']['protector'] % (self.player, self.target_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)

	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s" % (self.target_corporation.base_corporation.name)


class ExtractionOrder(OffensiveRunOrder):
	"""
	Model for Extraction Runs
	"""

	PROBA_SUCCESS = 10

	kidnapper_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve(self):
		if self.is_successful():
			if self.target_corporation.protectors.filter(done=True).count() >= 1 or randint(1, 100) <= self.target_corporation.kidnapper_protection:
				# succesful attack but defended
				self.resolve_interception()
			else:
				# Succesful attack
				self.resolve_success()
		else:
			# Attack failure
			if self.target_corporation.protectors.filter(done=True).count() >= 1 or randint(1, 100) <= self.target_corporation.kidnapper_protection:
				# Defense failure too
				self.resolve_fail()
			else:
				# Attack failure and successful defense
				self.resolve_capture

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = self.PROBA_SUCCESS
		if self.has_influence_bonus:
			proba += 30
		proba += self.additional_percents * 10

		return proba
	def resolve_success(self):
		self.target_corporation.assets -= 1
		self.target_corporation.save()

		self.kidnapper_corporation.assets += 1
		self.kidnapper_corporation.save()

		# Send a note for final message
		category = u"Run d'Extraction'"
		content = extraction_messages['success'] %(self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

	def resolve_fail(self):
		# Send a note for final message
		category = u"Run d'Extraction'"
		content = extraction_messages['fail'] %(self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

	def resolve_interception(self, po):
		# Send a note to the one who ordered the DataSteal
		category = u"Run d'Extraction'"
		content = extraction_messages['interception']['aggressor'] %(self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to the one who ordered the Protection
		category = u"Run de Protection"
		content = extraction_messages['interception']['protector'] %(self.target_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)

	def resolve_capture(self, po):
		# Send a note for final message
		category = u"Run d'Extraction'"
		content = extraction_messages['capture']['aggressor'] %(self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to the one who ordered the Protection
		category = u"Run de Protection"
		content = extraction_messages['capture']['protector'] %(self.player, self.target_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)

	def description(self):
		return u"Envoyer une équipe kidnapper un scientifique renommé de %s" %(self.target_corporation.base_corporation.name)


class ProtectionOrder(RunOrder):
	"""
	Model for Protection Runs
	"""
<<<<<<< HEAD
	title = "Lancer une run de Protection"

=======

	EXTRACTION = "ex"
	DATASTEAL = "ds"
	SABOTAGE = "sa"

	DEFENSE_CHOICES = (
		(EXTRACTION,"extraction"),
		(DATASTEAL, "datasteal"),
		(SABOTAGE, "sabotage")
	)
	defense = models.CharField(max_length=2, choices=DEFENSE_CHOICES)
>>>>>>> 6ce523f4826722081b958741fb55728c3c549059
	protected_corporation = models.ForeignKey(Corporation, related_name="protectors")
	done = models.BooleanField(default=False, editable=False)

	def resolve(self):
		if self.is_successful():
			self.resolve_successful()
			return True
		else:
			self.resolve_failure()
			return False

	def resolve_successful(self):
		self.done = True
		self.save()
		return True

	def resolve_failure(self):
		self.done = False

		return False

	def description(self):
		return u"Envoyer une équipe protéger les intérêts de %s" % (self.protected_corporation.base_corporation.name)

	def get_form(self, datas=None):
		form = super(ProtectionOrder, self).get_form(datas)
		form.fields['protected_corporation'].queryset = self.player.game.corporation_set.all()

		return form

orders = (DataStealOrder, ProtectionOrder, SabotageOrder, )
