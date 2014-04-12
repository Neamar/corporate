# -*- coding: utf-8 -*-
from django.db import models

from engine.models import Order, Player
from messaging.models import Message


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

		m = Message(
			title="Transfert d'argent",
			content="Un transfert de %s ¥ a été effectué de %s vers %s" % (self.amount, self.player, self.recipient),
			turn=self.player.game.current_turn,
			flag=Message.CASH_TRANSFER,
		)
		m.save()
		m.recipient_set.add(self.player, self.recipient)

	def get_cost(self):
		return self.amount

orders = (WiretransferOrder,)
