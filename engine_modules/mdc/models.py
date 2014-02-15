# -*- coding: utf-8 -*-
from django.db import models
from collections import Counter

from engine.models import Order, Game, Player


class MDCVoteOrder(Order):
	"""
	Order to vote for the party line of the MDC
	"""

	CPUB = "CPUB"
	CCIB = "CCIB"
	DERE = "DERE"
	DEVE = "DEVE"
	BANK = "BANK"
	TRAN = "TRAN"
	NONE = "NONE"

	# Enumerate the party lines and what they mean
	MDC_PARTY_LINE_CHOICES = (('CPUB', u'Contrats publics'),
		('CCIB', u'Contrôles ciblés'),
		('DERE', u'Dérégulation'),
		('DEVE', u'Développement urbain'),
		('BANK', u'Garde-fous bancaires'),
		('TRAN', u'Transparence'),
		('NONE', u'Pas de ligne officielle')
	)

	party_line = models.CharField(max_length=4, choices=MDC_PARTY_LINE_CHOICES, blank=True, null=True, default="NONE")

	def get_weight(self):
		"""
		returns the vote's weight: each corporation in which the player is top_shareholder (strictly more shares than any other)
					sides with said player, increasing the weight by 1
		each player also has their own vote
		"""
		return len(self.get_friendly_corporations()) + 1

	def get_friendly_corporations(self):

		vote_registry = self.build_vote_registry()
		if self.player in vote_registry.keys():
			return vote_registry[self.player]
		else:
			return []

	def build_vote_registry(self):
		"""
		Build a registry of the top shareholders for each corporation that will be used in calculation of weight
		"""
		vote_registry = {}
		corporations = self.player.game.corporation_set.all()
		for p in self.player.game.player_set.all():
			vote_registry[p] = []

		# For each corporation, get the 2 players that have the most shares
		for c in corporations:
			# We have to filter out the turns after that of the order, in case
			# the situation has changed since then
			shareholders = (s.player for s in c.share_set.filter(turn__lte=self.turn))
			top_holders = Counter(shareholders).most_common(2)
			# if they don't have the same number of shares, the first one gets a vote
			try:
				if top_holders[0][1] != top_holders[1][1]:
					vote_registry[top_holders[0][0]].append(c.base_corporation_slug)
			except(IndexError):
				if len(top_holders) != 0:
					# Only one has share
					vote_registry[top_holders[0][0]].append(c.base_corporation_slug)
		return vote_registry
	
	def description(self):
		return u"Voter pour définir la ligne du Manhattan Development Consortium"


class MDCVoteSession(models.Model):
	"""
	A session of the MDC voting process
	Used to keep track of the current MDC line
	"""

	current_party_line = models.CharField(max_length=4,
		choices=MDCVoteOrder.MDC_PARTY_LINE_CHOICES, blank=True, null=True, default=None)
	game = models.ForeignKey(Game)
	turn = models.PositiveSmallIntegerField(editable=False)

def get_current_mdc_party_line(self):
	"""
	Get the MDC party line voted last session
	if the current turn is the first one, returns "NONE"
	"""

	if self.current_turn == 1:
		return MDCVoteOrder.NONE

	session = self.mdcvotesession_set.get(turn=self.current_turn)
	return session.current_party_line

def get_last_mdc_vote(self):
	"""
	Get what a player voted in the last MDC Vote session
	"""

	try:
		vote = MDCVoteOrder.objects.get(turn=self.game.current_turn - 1, player=self)
	except:
		return MDCVoteOrder.NONE

	return vote.party_line

Game.get_current_mdc_party_line = get_current_mdc_party_line
Player.get_last_mdc_vote = get_last_mdc_vote
