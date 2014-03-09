# -*- coding: utf-8 -*-
from django.db import models

from engine.models import Order, Player


class WiretransferOrder(Order):
	"""
	Send money to another player.
	Immediate effect.
	"""
	title = "Envoyer de l'argent à un joueur"

	recipient = models.ForeignKey(Player)
	amount = models.PositiveIntegerField(help_text="En milliers de nuyens")

	def save(self, *args):
		# Override save: apply immediately and return
		self.player.money -= self.amount
		self.player.save()
		self.recipient.money += self.amount
		self.recipient.save()

	def get_cost(self):
		return self.amount

orders = (WiretransferOrder,)
