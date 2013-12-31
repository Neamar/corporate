# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Player, Order


class Influence(models.Model):
	"""
	Player influence level
	"""
	player = models.OneToOneField(Player)
	level = models.PositiveSmallIntegerField(default=1)


class BuyInfluenceOrder(Order):
	"""
	Order to increase Player Influence
	"""

	BASE_COST = 50

	def get_cost(self):
		return BuyInfluenceOrder.BASE_COST * (self.player.influence.level + 1)

	def resolve(self):
		# Pay.
		self.player.money -= self.get_cost()
		self.player.save()

		# Increase player influence by one
		self.player.influence.level += 1
		self.player.influence.save()

	def description(self):
		return u"Augmenter mon influence corporatiste à %s" % (self.player.influence.level + 1)


orders = (BuyInfluenceOrder,)
