# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator

from engine.models import Order
from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation

class OffensiveRunOrder(RunOrder):
	"""
	Model for DataSteal and Sabotage Runs
	Implements the check for Protection Runs
	"""

	target_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve_successful(self):
		protection = self.target_corporation.protectors.filter(done=False)
		for po in protection:
			# Test whether the Protection Run is successful
			if po.resolve():
				return self.resolve_interception(po)

		# No Protection Run has succeeded
		return self.resolve_success()

	def resolve_failure(self):
		protection = self.target_corporation.protectors.filter(done=False)
		for po in protection:
			# Test whether the Protection Run is successful
			if po.resolve():
				return self.resolve_capture(po)

		# No Protection Run has succeeded
		return self.resolve_fail()
		
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
	has_succeeded = False
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")	

	def resolve_success(self):
		
		self.stealer_corporation.assets += 1
		self.stealer_corporation.save()

		# Send a note for final message 
		title=u"Run de Datasteal"
		content=u"Votre équipe a réussi à voler des données de %s pour le compte de %s" %(self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

	def resolve_fail(self):
		
		# Send a note for final message
		title=u"Run de Datasteal"
		content=u"Votre équipe a échoué à voler %s pour le compte de %s mais a réussi à s'enfuir" %(self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

	def resolve_interception(self, po):
		# Send a note to the one who ordered the DataSteal
		title=u"Run de Datasteal"
		content=u"Votre équipe a été interceptée lors de la tentative de DataSteal sur %s. Elle a cependant réussi à s'enfuir" %(self.target_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)
		
		# Send a note to the one who ordered the Protection
		title=u"Run de Protection"
		content=u"Votre équipe a réussi à protéger %s d'une tentative de DataSteal. L'équipe adverse a cependant réussi à s'enfuir" %(po.protected_corporation)
		po.player.add_note(title=title, content=content)

	def resolve_capture(self, po):
		# Send a note to the one who ordered the DataSteal
		title=u"Run de Datasteal"
		content=u"Votre équipe a été capturée par une autre lors de la tentative de DataSteal sur %s. Le commanditaire est au courant de vos agissements" %(self.target_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)
		
		# Send a note to the one who ordered the Protection
		title=u"Run de Protection"
		content=u"Votre équipe a réussi à capturer une équipe de %s lors d'une tentative de DataSteal sur %s pour le compte de %s. L'équipe adverse a cependant réussi à s'enfuir" %(self.player.name, po.protected_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		po.player.add_note(title=title, content=content)
		
	def description(self):
		return u"Envoyer une équipe voler des données de %s pour le compte de %s" %(self.target_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)

class ProtectionOrder(RunOrder):
	"""
	Model for Protection Runs
	"""
	protected_corporation = models.ForeignKey(Corporation, related_name="protectors")
	done = models.BooleanField(default=False)

	def resolve_successful(self):
		self.done = True
		self.save()
		print "\nProtection Run should have succeeded"

		return True

	def resolve_failure(self):

		# This should enable the system to keep track of failed Protection Runs
		# and still distinguish between failed and successful Runs 
		# It will not, however, let you distinguish them after the turn has ended
		self.done = False
		print "\nProtection Run should have failed"

		return False

	def description(self):
		return u"Envoyer une équipe protéger les intérêts de %s" %(self.protected_corporation.base_corporation.name)

class SabotageOrder(OffensiveRunOrder):
	"""
	Model for Sabotage Runs
	"""

	def resolve_success(self):
		
		self.target_corporation.assets -= 2
		self.target_corporation.save()

		# Send a note for final message 
		title=u"Run de Sabotage"
		content=u"Votre équipe a réussi à saboter les opérations de %s" %(self.target_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)
		print "Sabotage Content : "
		print content

	def resolve_fail(self):
		
		# Send a note for final message 
		title=u"Run de Sabotage"
		content=u"La tentative de votre équipe pour saboter %s a échoué" %(self.target_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)
		print "Sabotage Content : "
		print content

	def resolve_interception(self, po):

		# Send a note to the one who ordered the DataSteal
		title=u"Run de Sabotage"
		content=u"Votre équipe a été inerceptée par une autre lors de la tentative de Sabotage sur %s. Elle a cependant réussi à s'enfuir" %(self.target_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

		# Send a note to the one who ordered the Protection
		title=u"Run de Protection"
		content=u"Votre équipe a réussi à protéger %s d'une tentative de DataSteal. L'équipe adverse a cependant réussi à s'enfuir" %(po.protected_corporation)
		po.player.add_note(title=title, content=content)
		print "Sabotage Content : "
		print content
	
	def resolve_capture(self, po):

		# Send a note for final message
		title=u"Capture"
		content=u"L'équipe que vous aviez envoyée saboter %s a été capturée" %(self.target_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

		# Send a note to the one who ordered the Protection
		title=u"Run de Protection"
		content=u"Votre équipe a réussi à capturer une équipe de %s lors d'une tentative de Sabotage sur %s. L'équipe adverse a cependant réussi à s'enfuir" %(self.player.name, po.protected_corporation.base_corporation.name)
		po.player.add_note(title=title, content=content)
		print "Sabotage Content : "
		print content
		
	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s" %(self.target_corporation.base_corporation.name)

orders = (DataStealOrder, ProtectionOrder, SabotageOrder, )
