# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator
from random import randint, shuffle

from engine.models import Order
from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation

class DataStealOrder(RunOrder):
	"""
	Model for DataSteal Runs
	"""
	has_succeeded = False
	stolen_corporation = models.ForeignKey(Corporation, related_name="+")	
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")	

		
	
	def resolve_successful(self):

		protected = shuffle(self.stolen_corporation.protecteurs.filter(done=False))
		protected = shuffle(self.stolen_corporation.protecteurs.all())
		print "Protected : "
		print protected

		if protected != None:
			po = protected[0]
			po.done = True
			po.save()

			# Send a note to the one who ordered the DataSteal
			title=u"Run de Datasteal"
			content=u"Votre équipe a été inerceptée par une autre lors de la tentative de DataSteal sur %s. Elle a cependant réussi à s'enfuir" %(self.stolen_corporation.base_corporation.name)
			self.player.add_note(title=title, content=content)

			# Send a note to the one who ordered the Protection
			title=u"Run de Protection"
			content=u"Votre équipe a réussi à protéger %s d'une tentative de DataSteal. L'équipe adverse a cependant réussi à s'enfuir" %(po.protected_corporation)
			po.player.add_note(title=title, content=content)
		else:
			self.stealer_corporation.assets += 1
			self.stealer_corporation.save()

			# Send a note for final message 
			title=u"Run de Datasteal"
			content=u"Votre équipe a réussi à voler des données de %s pour le compte de %s" %(self.stolen_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
			self.player.add_note(title=title, content=content)

	def resolve_failure(self):
		
		# Send a note for final message
		title=u"Run de Datasteal"
		content=u"La tentative de vol de données de votre équipe sur %s pour le compte de %s a échoué" %(self.stolen_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

	# The one who ordered the run should probably be made aware if his team got captured
	def resolve_capture(self):

		# Send a note for final message
		title=u"Capture"
		content=u"L'équipe que vous aviez envoyée pour voler des données à %s a été capturée" %(self.stolen_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)
		
	def description(self):
		return u"Envoyer une équipe voler des données de %s pour le compte de %s" %(self.stolen_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)

class ProtectionOrder(RunOrder):
	"""
	Model for Protection Runs
	"""
	protected_corporation = models.ForeignKey(Corporation, related_name="protecteurs")
	done = models.BooleanField(default=False)

	def resolve_successful(self):
		self.done = False
		self.save()

	def resolve_failure(self):

		# This should enable the system to keep track of failed Protection Runs
		# and still distinguish between failed and successful Runs 
		# It will not, however, let you distinguish them after the turn has ended
		self.done = True

		# Send a note for final message
		title=u"run de Protection"
		content=u"L'équipe que vous aviez envoyée protéger %s a échoué" %(self.protected_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

	def description(self):
		return u"Envoyer une équipe protéger les intérêts de %s" %(self.protected_corporation.base_corporation.name)

class SabotageOrder(RunOrder):
	"""
	Model for Sabotage Runs
	"""
	sabotaged_corporation = models.ForeignKey(Corporation, related_name="+")	

	def resolve_successful(self):

		protected = shuffle(self.sabotaged_corporation.protecteurs.filter(done=False))
		protected = shuffle(self.sabotaged_corporation.protecteurs.all())
		print "Sabotage Protected : "
		print protected

		if protected != None:
			po = protected[0]
			po.done = True
			po.save()

			# Send a note to the one who ordered the DataSteal
			title=u"Run de Sabotage"
			content=u"Votre équipe a été inerceptée par une autre lors de la tentative de Sabotage sur %s. Elle a cependant réussi à s'enfuir" %(self.sabotaged_corporation.base_corporation.name)
			self.player.add_note(title=title, content=content)

			# Send a note to the one who ordered the Protection
			title=u"Run de Protection"
			content=u"Votre équipe a réussi à protéger %s d'une tentative de DataSteal. L'équipe adverse a cependant réussi à s'enfuir" %(po.protected_corporation)
			po.player.add_note(title=title, content=content)
		else:
			self.sabotaged_corporation.assets -= 2
			self.sabotaged_corporation.save()

			# Send a note for final message 
			title=u"Run de Sabotage"
			content=u"Votre équipe a réussi à saboter les opérations de %s" %(self.sabotaged_corporation.base_corporation.name)
			self.player.add_note(title=title, content=content)

	def resolve_failure(self):

		# Send a note for final message 
		title=u"Run de Sabotage"
		content=u"La tentative de votre équipe pour saboter %s a échoué" %(self.sabotaged_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

	def resolve_capture(self):
		"""
		The one who ordered the run should probably be made aware if his team got captured
		"""

		# Send a note for final message
		title=u"Capture"
		content=u"L'équipe que vous aviez envoyée saboter %s a été capturée" %(self.sabotaged_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)
		
	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s" %(self.sabotaged_corporation.base_corporation.name)

orders = (DataStealOrder, ProtectionOrder, SabotageOrder, )
