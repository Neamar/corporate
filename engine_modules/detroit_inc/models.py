# -*- coding: utf-8 -*-
from collections import Counter
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from engine.models import Order, Game, Player
from website.widgets import PlainTextField


class DIncVoteOrder(Order):
	"""
	Order to vote for the Detroit, Inc. coalition
	"""
	ORDER = 200

	CPUB = "CPUB"
	RSEC = "RSEC"
	CONS = "CONS"

	# @Neamar: Why is DINC_COALTION_CHOICES not a dict ?
	# Enumerate the party lines and their meanings
	DINC_COALITION_CHOICES = (
		('CPUB', 'Contrats publics'),
		('RSEC', u'Réforme de la sécurité'),
		('CONS', 'Consolidation'),
	)

	DINC_OPPOSITIONS = {
		CPUB: RSEC,
		RSEC: CONS,
		CONS: CPUB,
	}

	title = "Choisir une coalition"

	coalition = models.CharField(max_length=4, choices=DINC_COALITION_CHOICES, blank=True, null=True, default=None)

	def get_weight(self):
		"""
		Return the vote's weight: each corporation in which the player is top_shareholder (strictly more shares than any other), plus one (each player has a voice)
		"""
		return len(self.get_friendly_corporations()) + 1

	def get_friendly_corporations(self):
		"""
		Find all corporations where the player is top shareholder.
		"""
		return self.vote_registry[self.player]

	@cached_property
	def vote_registry(self):
		"""
		Build a registry of the top shareholders for each corporation that will be used in calculation of weight
		"""
		vote_registry = {}
		corporations = self.player.game.corporation_set.all()
		for p in self.player.game.player_set.all():
			vote_registry[p] = []

		# For each corporation, get the 2 players that have the most shares
		for c in corporations.prefetch_related('share_set'):
			# Filter to shares bought up to the turn this order was passed
			shareholders = (s.player for s in c.share_set.filter(turn__lte=self.player.game.current_turn).prefetch_related('player'))
			top_holders = Counter(shareholders).most_common(2)
			try:
				# if they don't have the same number of shares, the first one gets a vote
				if top_holders[0][1] != top_holders[1][1]:
					vote_registry[top_holders[0][0]].append(c)
			except IndexError:
				if len(top_holders) != 0:
					# Only one has share
					vote_registry[top_holders[0][0]].append(c)
		return vote_registry

	def get_form(self, data=None):
		form = super(DIncVoteOrder, self).get_form(data)
		form.fields['coalition_weight'] = PlainTextField(initial=str(self.get_weight()))
		form.fields['coalition_weight'].label = u'Votre poids'

		return form

	def get_form_class(self):
		ParentOrderForm = super(DIncVoteOrder, self).get_form_class()

		class OrderForm(ParentOrderForm):
			def clean_coalition(self):
				if self.cleaned_data['coalition'] is None:
					raise ValidationError("Vous devez choisir une coalition.")
				return self.cleaned_data['coalition']

		return OrderForm

	def description(self):
		return u"Apporter %d voix pour la coalition « %s » de Detroit, Inc." % (self.get_weight(), self.get_coalition_display())


class DIncVoteSession(models.Model):
	"""
	A session of the Detroit, Inc. voting process
	Used to keep track of the current Detroit, Inc line
	"""

	coalition = models.CharField(max_length=4,
		choices=DIncVoteOrder.DINC_COALITION_CHOICES, blank=True, null=True, default=None)
	game = models.ForeignKey(Game)
	turn = models.PositiveSmallIntegerField(editable=False)

	def __unicode__(self):
		return u"%s line for %s on turn %s" % (self.coalition, self.game, self.turn)


def get_dinc_coalition(self, turn=None):
	"""
	Get the Detroit, Inc. party line voted on turn session (defaults to current turn).
	Return None on the first turn.
	"""

	if turn is None:
		turn = self.current_turn

	try:
		session = self.dincvotesession_set.get(turn=turn)
	except DIncVoteSession.DoesNotExist:
		return None
	return session.coalition


def get_last_dinc_vote(self):
	"""
	Get what a player voted in the last Detroit, Inc. Vote session
	"""

	try:
		return DIncVoteOrder.objects.get(turn=self.game.current_turn - 1, player=self)
	except:
		# No vote
		return None


def get_last_dinc_coalition(self):
	"""
	Get what a player voted in the last Detroit, Inc. Vote session
	"""

	vote = self.get_last_dinc_vote()
	if vote:
		return vote.coalition
	else:
		return None

Game.get_dinc_coalition = get_dinc_coalition
Player.get_last_dinc_vote = get_last_dinc_vote
Player.get_last_dinc_coalition = get_last_dinc_coalition

orders = (DIncVoteOrder,)
