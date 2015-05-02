# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Player, Order, Game
from messaging.models import Newsfeed


class Influence(models.Model):
	"""
	Player influence level
	"""
	class Meta:
		unique_together = (("player", "turn"),)

	player = models.ForeignKey(Player)
	turn = models.PositiveSmallIntegerField(default=1)
	level = models.PositiveSmallIntegerField(default=1)


class BuyInfluenceOrder(Order):
	"""
	Order to increase Player Influence
	"""
	ORDER = 300
	BASE_COST = 400
	title = "Acheter un point d'Influence Corporatiste"

	def get_cost(self):
		return BuyInfluenceOrder.BASE_COST * (self.player.influence.level + 1)

	def resolve(self):
		# Pay.
		self.player.money -= self.get_cost()
		self.player.save()

		# Increase player influence by one
		influence = self.player.influence_set.get(turn=self.turn)
		influence.level += 1
		influence.save()

		# Create game event
		self.player.game.create_game_event(event_type=Game.IC_UP, data='', players=[self.player])

		# Send a note for final message
		content = u"Votre Influence dans le milieu corporatiste monte à %i." % self.player.influence.level
		self.player.add_note(content=content)

		# Newsfeed
		newsfeed_content = u"L'Influence Corporatiste de %s monte à %i." % (self.player.name, self.player.influence.level)
		self.player.game.add_newsfeed(category=Newsfeed.PEOPLE, content=newsfeed_content, players=[self.player], status=Newsfeed.PUBLIC)

	def description(self):
		return u"Augmenter mon Influence Corporatiste à %s" % (self.player.influence.level + 1)


orders = (BuyInfluenceOrder,)
