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

	# Enumerate the party lines and their meanings
	MDC_PARTY_LINE_CHOICES = (('CPUB', u'Contrats publics'),
		('CCIB', u'Contrôles ciblés'),
		('DERE', u'Dérégulation'),
		('DEVE', u'Développement urbain'),
		('BANK', u'Garde-fous bancaires'),
		('TRAN', u'Transparence'),
	)
	title = "Choisir une coalition"

	party_line = models.CharField(max_length=4, choices=MDC_PARTY_LINE_CHOICES, blank=True, null=True, default=None)

	def get_weight(self):
		"""
		Return the vote's weight: each corporation in which the player is top_shareholder (strictly more shares than any other), plus one (each player has a voice)
		"""
		return len(self.get_friendly_corporations()) + 1

	def get_friendly_corporations(self):
		"""
		Find all corporations where the player is top shareholder.
		"""
		vote_registry = self.build_vote_registry()
		return vote_registry[self.player]

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
			try:
				# if they don't have the same number of shares, the first one gets a vote
				if top_holders[0][1] != top_holders[1][1]:
					vote_registry[top_holders[0][0]].append(c.base_corporation_slug)
			except(IndexError):
				if len(top_holders) != 0:
					# Only one has share
					vote_registry[top_holders[0][0]].append(c.base_corporation_slug)
		return vote_registry

	def description(self):
		return u"Apporter %d voix pour la coalition « %s » du MDC" % (self.get_weight(), self.get_party_line_display())


class MDCVoteSession(models.Model):
	"""
	A session of the MDC voting process
	Used to keep track of the current MDC line
	"""

	party_line = models.CharField(max_length=4,
		choices=MDCVoteOrder.MDC_PARTY_LINE_CHOICES, blank=True, null=True, default=None)
	game = models.ForeignKey(Game)
	turn = models.PositiveSmallIntegerField(editable=False)

	def __unicode__(self):
		return "%s line for %s on turn %s" % (self.party_line, self.game, self.turn)


def get_mdc_party_line(self, turn=None):
	"""
	Get the MDC party line voted on turn session (defaults to current turn).
	Return None on the first turn.
	"""
	if turn is None:
		turn = self.current_turn

	if turn == 1:
		return None

	session = self.mdcvotesession_set.get(turn=turn)
	return session.party_line


def get_last_mdc_vote(self):
	"""
	Get what a player voted in the last MDC Vote session
	"""

	try:
		vote = MDCVoteOrder.objects.get(turn=self.game.current_turn - 1, player=self)
		return vote.party_line
	except:
		# No vote
		return None


Game.get_mdc_party_line = get_mdc_party_line
Player.get_last_mdc_vote = get_last_mdc_vote

orders = (MDCVoteOrder,)
