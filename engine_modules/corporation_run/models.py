# -*- coding: utf-8 -*-
from django.db import models

from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation

DEBUG = False

datasteal_messages = 	{'success'	: u"Votre équipe a réussi à voler des données de {0} pour le compte de {1}",
			 'fail'		: u"Votre équipe a échoué lors de la tentative de DataSteal sur {0} pour {1}",
			 'interception'	: { 'aggressor'	: u"Votre équipe a été interceptée lors de la tentative de DataSteal sur {0}. Elle a cependant réussi à s'enfuir",
					    'protector'	: u"Votre équipe a réussi à protéger {0} d'une tentative de DataSteal. L'équipe adverse a cependant réussi à s'enfuir",
					},
			 'capture'	: { 'aggressor' : u"Votre équipe a été capturée par une autre lors de la tentative de DataSteal sur {0}. Le commanditaire est au courant de vos agissements",
					    'protector'	: u"Votre équipe a réussi à capturer une équipe de {0} lors d'une tentative de DataSteal sur {1} pour le compte de {2}.",
					},
			 'late'		: u"Votre équipe s'est introduite chez {0} mais n'a pas trouvé de donées intéressantes pour {1}"
}

sabotage_messages = 	{'success'	: u"Votre équipe a réussi à saboter les opérations de {0}",
			 'fail'		: u"La tentative de votre équipe pour saboter {0} a échoué",
			 'interception'	: { 'aggressor'	: u"Votre équipe a été inerceptée par une autre lors de la tentative de Sabotage sur {0}. Elle a cependant réussi à s'enfuir",
					    'protector'	: u"Votre équipe a réussi à protéger {0} d'une tentative de Sabotage. L'équipe adverse a cependant réussi à s'enfuir",
					},
			'capture'	: { 'aggressor' : u"L'équipe que vous aviez envoyée saboter {0} a été capturée",
					    'protector'	: u"Votre équipe a réussi à capturer une équipe de {0} lors d'une tentative de Sabotage sur {1}",
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

	target_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve_successful(self):
		if DEBUG : print "resolve_successful OffRunOrder"
		# The Protection Runs must be tested from highest to lowest probability of success
		protection = sorted(self.target_corporation.protectors.filter(done=False), key=lambda po: po.get_success_probability(), reverse=True)
		for po in protection:
			# Test whether the Protection Run is successful
			if po.resolve():
				if DEBUG : print "Protection has succeeded !!!!"
				return self.resolve_interception(po)

		# No Protection Run has succeeded
		if DEBUG : print "All Protections have failed !!!!"
		self.resolve_success()
		return True

	def resolve_failure(self):
		if DEBUG : print "resolve_failure OffRunOrder"
		protection = sorted(self.target_corporation.protectors.filter(done=False), key=lambda po: po.get_success_probability(), reverse=True)
		for po in protection:
			# Test whether the Protection Run is successful
			if po.resolve():
				if DEBUG : print "Protection has succeeded !!!!"
				return self.resolve_capture(po)

		# No Protection Run has succeeded
		if DEBUG : print "All Protections have failed !!!!"
		self.resolve_fail()
		return False

	def resolve_success(self):
		"""
		This method is called when the Offensive Run succeeds on a corporation 
		that has no successful Protection Run.

		It must be overriden
		"""
		raise NotImplementedError()
	
	def resolve_fail(self):
		"""
		This method is called when the Offensive Run fails on a corporation 
		that has no successful Protection Run.

		It must be overriden
		"""
		raise NotImplementedError()

	def resolve_interception(self, po):
		"""
		This method is called when the Offensive Run succeeds on a corporation 
		that has a successful Protection Run.

		It must be overriden
		"""
		raise NotImplementedError()

	def resolve_capture(self, po):
		"""
		This method is called when the Offensive Run fails on a corporation 
		that has a successful Protection Run.

		It must be overriden
		"""
		raise NotImplementedError()


class DataStealOrder(OffensiveRunOrder):
	"""
	Model for DataSteal Runs
	"""
	has_succeeded = models.BooleanField(default=False)
	# Same as OffensiveRunOrder.target_corporation, but we have to put it here to be able to
	# backtrace the relation only to DataSteals and not all Offensive Runs
	stolen_corporation = models.ForeignKey(Corporation, related_name="thieves", null=True, blank=True)
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")	

	# This is kind of a complicated hack, but it is necessary for the same reason stolen_corporation is
	# It makes creating DataSteals a bit easier (no duplication of info between stolen_corporation and target_corporation at creation)
	def __init__(self, *args, **kwargs):
		if "stealer_corporation" in kwargs.keys():
			stealer_corporation = kwargs.pop("stealer_corporation")
			super(DataStealOrder, self).__init__(*args, **kwargs)
			self.stolen_corporation = self.target_corporation
			self.stealer_corporation = stealer_corporation
		else:
			super(DataStealOrder, self).__init__(*args, **kwargs)

	def resolve_success(self):
		if DEBUG : print "resolve_success DataSteal"
		thief = self.target_corporation.thieves.filter(has_succeeded=True)
		if len(thief) != 0:
			# Send a note for final message 
			category=u"Run de Datasteal"
			content=datasteal_messages['late'].format(self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
			self.player.add_note(category=category, content=content)
			
		else:
			self.has_succeeded = True
			self.save()
			self.stealer_corporation.assets += 1
			self.stealer_corporation.save()

			# Send a note for final message 
			category=u"Run de Datasteal"
			content=datasteal_messages['success'].format(self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
			self.player.add_note(category=category, content=content)
		return True

	def resolve_fail(self):
		
		if DEBUG : print "resolve_fail DataSteal"
		# Send a note for final message
		category=u"Run de Datasteal"
		content=datasteal_messages['fail'].format(self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

	def resolve_interception(self, po):
		if DEBUG : print "resolve_interception DataSteal"
		# Send a note to the one who ordered the DataSteal
		category=u"Run de Datasteal"
		content=datasteal_messages['interception']['aggressor'].format(self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)
		
		# Send a note to the one who ordered the Protection
		category=u"Run de Protection"
		content=datasteal_messages['interception']['protector'].format(self.target_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)

	def resolve_capture(self, po):
		if DEBUG : print "resolve_capture DataSteal"
		# Send a note to the one who ordered the DataSteal
		category=u"Run de Datasteal"
		content=datasteal_messages['capture']['aggressor'].format(self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)
		
		# Send a note to the one who ordered the Protection
		category=u"Run de Protection"
		content=datasteal_messages['capture']['protector'].format(self.player.name, self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)
		
	def description(self):
		return u"Envoyer une équipe voler des données de %s pour le compte de %s" %(self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)

class DefensiveRunOrder(RunOrder):
	
	class Meta:
		proxy = True

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()
		
		if self.is_successful():
			if DEBUG : print "DefensiveRunOrder Successful"
			self.resolve_successful()
			return True
		else:
			if DEBUG : print "DefensiveRunOrder Fail"
			self.resolve_failure()
			return False

class ProtectionOrder(DefensiveRunOrder):

	"""
	Model for Protection Runs
	"""
	protected_corporation = models.ForeignKey(Corporation, related_name="protectors")
	done = models.BooleanField(default=False)

	def resolve_successful(self):
		
		if DEBUG : print "resolve_successful Protection"
		self.done = True
		self.save()
		return True

	def resolve_failure(self):

		if DEBUG : print "resolve_failure Protection"
		self.done = False

		return False

	def description(self):
		return u"Envoyer une équipe protéger les intérêts de %s" %(self.protected_corporation.base_corporation.name)


class SabotageOrder(OffensiveRunOrder):
	"""
	Model for Sabotage Runs
	"""

	def resolve_success(self):
		
		if DEBUG : print "resolve_sucess Sabotage"
		self.target_corporation.assets -= 2
		self.target_corporation.save()

		# Send a note for final message 
		category=u"Run de Sabotage"
		content=sabotage_messages['success'].format(self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

	def resolve_fail(self):
		
		if DEBUG : print "resolve_fail Sabotage"
		# Send a note for final message 
		category=u"Run de Sabotage"
		content=sabotage_messages['fail'].format(self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

	def resolve_interception(self, po):

		if DEBUG : print "resolve_interception Sabotage"
		# Send a note to the one who ordered the DataSteal
		category=u"Run de Sabotage"
		content=sabotage_messages['interception']['aggressor'].format(self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to the one who ordered the Protection
		category=u"Run de Protection"
		content=sabotage_messages['interception']['protector'].format(self.target_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)
	
	def resolve_capture(self, po):

		if DEBUG : print "resolve_capture Sabotage"
		# Send a note for final message
		category=u"Run de Sabotage"
		content=sabotage_messages['capture']['aggressor'].format(self.target_corporation.base_corporation.name)
		self.player.add_note(category=category, content=content)

		# Send a note to the one who ordered the Protection
		category=u"Run de Protection"
		content=sabotage_messages['capture']['protector'].format(self.player, self.target_corporation.base_corporation.name)
		po.player.add_note(category=category, content=content)
		
	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s" %(self.target_corporation.base_corporation.name)

orders = (DataStealOrder, ProtectionOrder, SabotageOrder, )
