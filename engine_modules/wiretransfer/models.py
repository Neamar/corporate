# -*- coding: utf-8 -*-
from django.db import models

from engine.models import Order, Player, Game
from messaging.models import Message
from messaging.models import Newsfeed


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
			content="Un transfert de %s k¥ a été effectué de %s vers %s" % (self.amount, self.player, self.recipient),
			turn=self.player.game.current_turn,
			flag=Message.CASH_TRANSFER,
		)
		m.save()
		m.recipient_set.add(self.player, self.recipient)

		# Newsfeed
		content = u"%s a donné %s k¥ à %s." % (self.player, self.amount, self.recipient)
		players = [self.player, self.recipient]
		self.player.game.add_newsfeed(category=Newsfeed.ECONOMY, content=content, status=Newsfeed.PRIVATE, players=players)

		# Create the game_event
		self.player.game.add_event(event_type=Game.WIRETRANSFER, data='', players=[self.player, self.recipient])

	def get_cost(self):
		# or 1: avoid displaying the order without money
		return self.amount or 1

orders = (WiretransferOrder,)
