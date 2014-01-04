# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator
from random import randint

from engine.models import Order
from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation

class DataStealOrder(RunOrder):
	"""
	Model for DataSteal Runs
	"""
	stolen_corporation = models.ForeignKey(Corporation, related_name="+")	
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")	

	def resolve_successful(self):

		self.stealer_corporation.assets += 1
		self.stealer_corporation.save()
	
		#Send a note for final message 
		title=u"Run de Datasteal"
		content=u"Votre équipe a réussi à voler des données de %s pour le compte de %s" %(self.stolen_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

	def resolve_failure(self):
		
		#Send a note for final message
		title=u"Run de Datasteal"
		content=u"La tentative de vol de données de votre équipe sur %s pour le compte de %s a échoué" %(self.stolen_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

	# The one who ordered the run should probably be made aware if his team got captured
	def resolve_capture(self):

		#Send a note for final message
		title=u"Capture"
		content=u"L'équipe que vous aviez envoyée pour voler des données à %s a été capturée"
		self.player.add_note(title=title, content=content) %(self.stolen_corporation.base_corporation.name)
		
	def description(self):
		return u"Envoyer une équipe voler des données de %s pour le compte de %s" %(self.stolen_corporation.base_corporation.name, self.stealer_corporation.base_corporation.name)

class ProtectionOrder(RunOrder):
	"""
	Model for Protection Runs
	"""
	protected_corporation = models.ForeignKey(Corporation, related_name="+")

	def resolve_successful(self):
		pass
	def resolve_failure(self):
		pass
	def description(self):
		return u"Envoyer une équipe protéger les intérêts de %s" %(self.protected_corporation.base_corporation.name)

class SabotageOrder(RunOrder):
	"""
	Model for Sabotage Runs
	"""
	sabotaged_corporation = models.ForeignKey(Corporation, related_name="+")	

	def resolve_successful(self):

		self.sabotaged_corporation.assets -= 2
		self.sabotaged_corporation.save()

		#Send a note for final message 
		title=u"Run de Sabotage"
		content=u"Votre équipe a réussi à saboter les opérations de %s" %(self.sabotaged_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)

	def resolve_failure(self):

		#Send a note for final message 
		title=u"Run de Sabotage"
		content=u"La tentative de votre équipe pour saboter %s a échoué" %(self.sabotaged_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)
	"""
	The one who ordered the run should probably be made aware if his team got captured
	"""
	def resolve_capture(self):

		#Send a note for final message
		title=u"Capture"
		content=u"L'équipe que vous aviez envoyée saboter %s a été capturée" %(self.sabotaged_corporation.base_corporation.name)
		self.player.add_note(title=title, content=content)
		
	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s" %(self.sabotaged_corporation.base_corporation.name)

orders = (DataStealOrder, ProtectionOrder, SabotageOrder, )
