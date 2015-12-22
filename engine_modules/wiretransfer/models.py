# -*- coding: utf-8 -*-
from django.db import models

from engine.models import Order, Player, Game


class WiretransferOrder(Order):
	"""
	Send money to another player.
	Immediate effect.
	"""
	ORDER = 1100
	title = "Envoyer de l'argent à un joueur"

	recipient = models.ForeignKey(Player)
	amount = models.PositiveIntegerField(help_text="En milliers de nuyens")

	def save(self, *args):
		# Override save: apply immediately and return
		self.player.money -= self.amount
		self.player.save()
		self.recipient.money += self.amount
		self.recipient.save()

		# Create the game_event
		self.player.game.add_event(event_type=Game.WIRETRANSFER, data={"giver": self.player.name, "receiver": self.recipient.name, "money": self.amount}, players=[self.player, self.recipient])

	def get_cost(self):
		# or 1: avoid displaying the order without money
		return self.amount or 1

	def get_form(self, data=None):
		form = super(WiretransferOrder, self).get_form(data)
		form.fields['recipient'].queryset = Player.objects.filter(game=self.player.game).exclude(pk=self.player.pk)
		return form

orders = (WiretransferOrder,)
