# -*- coding: utf-8 -*-
from django.db import models
from collections import Counter

from engine.models import Order, Game
from engine.exceptions import OrderNotAvailable


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
		('TRAN', u'Transparence')
	)

	title = "Choisir une coalition"

	party_line = models.CharField(max_length=4, choices=MDC_PARTY_LINE_CHOICES, blank=True, null=True, default=None)

	def get_weight(self):

		vote_registry = self.build_vote_registry()
		if self.player in vote_registry.values():
			return Counter(vote_registry.values())[self.player] + 1
		else:
			return 1

	def build_vote_registry(self):
		"""
		Build a registry of the top shareholders for each corporation that will be used in calculation of weight
		"""
		vote_registry = {}
		corporations = self.player.game.corporation_set.all()
		# For each corporation, get the 2 players that have the most shares
		for c in corporations:
			shareholders = (s.player for s in c.share_set.all())
			top_holders = Counter(shareholders).most_common(2)
			# if they don't have the same number of shares, the first one gets a vote
			try:
				if top_holders[0][1] != top_holders[1][1]:
					vote_registry[c.base_corporation_slug] = top_holders[0][0]
			except(IndexError):
				if len(top_holders) != 0:
					# Only one has share
					vote_registry[c.base_corporation_slug] = top_holders[0][0]
		return vote_registry

	def description(self):
		return u"Apporter %d voix pour la coalition « %s » du MDC" % (self.get_weight(), self.get_party_line_display())


class MDCVoteSession(models.Model):
	"""
	A session of the MDC voting process
	Used to keep track of the current MDC line
	"""

	current_party_line = models.CharField(max_length=3,
		choices=MDCVoteOrder.MDC_PARTY_LINE_CHOICES, blank=True, null=True, default=None)
	game = models.ForeignKey(Game)
	turn = models.PositiveSmallIntegerField(editable=False)

orders = (MDCVoteOrder,)
