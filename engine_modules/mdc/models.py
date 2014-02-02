# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from collections import Counter

from engine.models import Order, Game
from engine_modules.corporation.models import Corporation


	
class MDCVoteOrder(Order):
	"""
	Order to vote for the party line of the MDC
	"""

	# Enumerate the party lines and what they mean
	MDC_PARTY_LINE_CHOICES = (('CPUB', u'Contrats publics'), 
				('CCIB', u'Contrôles ciblés'), 
				('DERE', u'Dérégulation'), 
				('DEVE', u'Développement urbain'), 
				('BANK', u'Garde-fous bancaires'), 
				('TRAN', u'Transparence'), 
				('NONE', u'Aucune'))

	weight = models.PositiveSmallIntegerField(default=1)
	party_line = models.CharField(max_length=4, 
				choices=MDC_PARTY_LINE_CHOICES,
				default = "NONE")

	def resolve(self, vote_registry):

		if self.player in vote_registry.values():
			self.weight = Counter(vote_registry.values())[self.player]+1
			self.save()

	@classmethod
	def build_vote_registry(cls, game):
		"""
		Build a registry of the top shareholders for each corporation that will be 
		used in resolve, but must be exported in order to be calculated only once
		"""
		vote_registry = {}
		corporations = game.corporation_set.all()
		for c in corporations:
			shareholders  = (s.player for s in c.share_set.all())
			top_holders = Counter(shareholders).most_common(2)
			try:
				if top_holders[0][1] != top_holders[1][1]:
					vote_registry[c.base_corporation_slug] = top_holders[0][0]
			except(IndexError):
				if len(top_holders) != 0:
					vote_registry[c.base_corporation_slug] = top_holders[0][0]
		return vote_registry
	
	def description(self):
		return u"Vote pour définir la ligne du Manhattan Development Consortium"

class MDCVoteSession(models.Model):
	"""
	A session of the MDC voting process
	Used to keep track of the current MDC line
	"""

	current_party_line = models.CharField(max_length=3,
				choices=MDCVoteOrder.MDC_PARTY_LINE_CHOICES,
				default="NONE")
	game = models.ForeignKey(Game)
	turn = models.PositiveSmallIntegerField(editable=False)
