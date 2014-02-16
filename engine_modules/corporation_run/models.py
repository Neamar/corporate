# -*- coding: utf-8 -*-
from django.db import models

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

	def resolve_successful(self):
		# The Protection Runs must be tested from highest to lowest probability of success
		protection_runs = sorted(self.target_corporation.protectors.filter(done=False), key=lambda po: po.get_success_probability(), reverse=True)
		for protection_run in protection_runs:
			# Test whether the Protection Run is successful
			if protection_run.resolve():
				return self.resolve_interception(protection_run)

		# No Protection Run has succeeded
		self.resolve_success()
		return True

	def resolve_failure(self):
		protection_runs = sorted(self.target_corporation.protectors.filter(done=False), key=lambda po: po.get_success_probability(), reverse=True)
		for protection_run in protection_runs:
			# Test whether the Protection Run is successful
			if protection_run.resolve():
				return self.resolve_capture(protection_run)

		# No Protection Run has succeeded
		self.resolve_fail()
		return False

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
	title = "Lancer une run de Datasteal"
	
	has_succeeded = models.BooleanField(default=False, editable=False)
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")

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


class DefensiveRunOrder(RunOrder):
	"""
	Model for defensive corporation runs.

	Resolve the runs in a slightly different way thant standards run.
	"""
	class Meta:
		proxy = True

	def resolve(self):
		
		if self.is_successful():
			self.resolve_successful()
			return True
		else:
			self.resolve_failure()
			return False


class ProtectionOrder(DefensiveRunOrder):
	"""
	Model for Protection Runs
	"""
	title = "Lancer une run de Protection"

	protected_corporation = models.ForeignKey(Corporation, related_name="protectors")
	done = models.BooleanField(default=False, editable=False)

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
