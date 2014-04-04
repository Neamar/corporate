# -*- coding: utf-8 -*-
from collections import Counter
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from engine.models import Order, Game, Player
from website.widgets import PlainTextField


class MDCVoteOrder(Order):
	"""
	Order to vote for the MDC coalition
	"""

	CPUB = "CPUB"
	CCIB = "CCIB"
	DERE = "DERE"
	DEVE = "DEVE"
	BANK = "BANK"
	TRAN = "TRAN"

	# Enumerate the party lines and their meanings
	MDC_COALITION_CHOICES = (
		(
			'Contrats publics / Développement urbain',
			(
				('CPUB', 'Contrats publics'),
				('DEVE', u'Développement urbain'),
			)
		),
		(
			'Contrôles ciblés / Transparence',
			(
				('CCIB', 'Contrôles ciblés'),
				('TRAN', u'Transparence'),
			)
		),
		(
			'Garde-fous bancaires / Dérégulation',
			(
				('BANK', u'Garde-fous bancaires'),
				('DERE', u'Dérégulation'),
			)
		),
	)

	MDC_OPPOSITIONS = {
		CPUB: DEVE,
		DEVE: CPUB,
		CCIB: TRAN,
		TRAN: CCIB,
		BANK: DERE,
		DERE: BANK
	}

	title = "Choisir une coalition"

	coalition = models.CharField(max_length=4, choices=MDC_COALITION_CHOICES, blank=True, null=True, default=None)

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
		for c in corporations:
			# Filter to shares bought up to the turn this order was passed + 1
			shareholders = (s.player for s in c.share_set.filter(turn__lte=self.player.game.current_turn + 1))
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

	def get_form(self, datas=None):
		form = super(MDCVoteOrder, self).get_form(datas)
		form.fields['coalition_weight'] = PlainTextField(initial=str(self.get_weight()))

		return form

	def get_form_class(self):
		ParentOrderForm = super(MDCVoteOrder, self).get_form_class()

		class OrderForm(ParentOrderForm):
			def clean_coalition(self):
				if self.cleaned_data['coalition'] is None:
					raise ValidationError("Vous devez choisir une coalition.")
				return self.cleaned_data['coalition']

		return OrderForm

	def description(self):
		return u"Apporter %d voix pour la coalition « %s » du MDC" % (self.get_weight(), self.get_coalition_display())


class MDCVoteSession(models.Model):
	"""
	A session of the MDC voting process
	Used to keep track of the current MDC line
	"""

	coalition = models.CharField(max_length=4,
		choices=MDCVoteOrder.MDC_COALITION_CHOICES, blank=True, null=True, default=None)
	game = models.ForeignKey(Game)
	turn = models.PositiveSmallIntegerField(editable=False)

	def __unicode__(self):
		return "%s line for %s on turn %s" % (self.coalition, self.game, self.turn)


def get_mdc_coalition(self, turn=None):
	"""
	Get the MDC party line voted on turn session (defaults to current turn).
	Return None on the first turn.
	"""
	if turn is None:
		turn = self.current_turn

	if turn == 1:
		return None

	session = self.mdcvotesession_set.get(turn=turn)
	return session.coalition


def get_last_mdc_vote(self):
	"""
	Get what a player voted in the last MDC Vote session
	"""

	try:
		vote = MDCVoteOrder.objects.get(turn=self.game.current_turn - 1, player=self)
		return vote.coalition
	except:
		# No vote
		return None


Game.get_mdc_coalition = get_mdc_coalition
Player.get_last_mdc_vote = get_last_mdc_vote

orders = (MDCVoteOrder,)
