# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from collections import Counter

from engine.models import Order, Game
from engine_modules.corporation.models import Corporation

# Enumerate the party lines and what they mean
MDC_Party_Lines = {"cpublics": (u"Contrats publics", u"redistribution des contrats pblics de Manhattan"), 
		"ccibles": (u"Contrôles ciblés", u"Implémentation de contrôles spécifiques sur des sujets sensibles"), 
		"deregulation": (u"Dérégulation", u"Affaiblissement des contrôles et législations en places\
qui freinent l'essor de Manhattan"), 
		"developpement": (u"Développement urbain", u"Grand projet de rénovation et d'aménagement de \
l'aire urbaine"), 
		"banques": (u"Garde-fous bancaires", u"Réduction des libertés des banques et lobbying pour \
l'empêchement de l'hyperspéculation"), 
		"transparence": (u"Transparence", u"Mesures visant à réduire l'opacité du processus décisionnel"),
		"aucune": (u"Aucune", u"Le MDC n'est pas parvenu à établir une ligne politique officielle")
}


class MDCVoteSession(models.Model):
	"""
	A session of the MDC voting process
	Used to keep track of the current MDC line
	"""

	current_party_line = models.CharField(max_length=50)
	game = models.ForeignKey(Game)
	turn = models.PositiveSmallIntegerField(editable=False)
	
class MDCVoteOrder(Order):
	"""
	Order to vote for the party line of the MDC
	"""

	weight = models.PositiveSmallIntegerField(default=1)
	party_line = models.CharField(max_length=30)

	def resolve(self, vote_registry):
		if self.party_line not in MDC_Party_Lines.keys():
			raise ValidationError

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
				if(len(top_holders) != 0):
					vote_registry[c.base_corporation_slug] = top_holders[0][0]
		return vote_registry
	
	def description(self):
		return u"Vote pour définir la ligne du Manhattan Development Consortium"
