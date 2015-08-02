# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Player, Order, Game
from engine_modules.corporation.models import Corporation


class Share(models.Model):
	"""
	A share held by some player
	"""
	corporation = models.ForeignKey(Corporation)
	player = models.ForeignKey(Player)
	turn = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return u"%s share for %s" % (self.corporation, self.player)


class BuyShareOrder(Order):
	"""
	Order to buy a corporation share
	"""
	title = "Acheter une part dans une corporation"
	ORDER = 100
	BASE_COST = 100
	FIRST_COST = 125
	FIRST_AND_CITIZEN_COST = 100

	corporation = models.ForeignKey(Corporation)

	def get_cost(self):
		if not hasattr(self, "corporation"):
			# 1: avoid displaying the order when the player has no money left
			return 1
		elif self.corporation == self.player.game.get_ladder()[0]:
			if self.player.citizenship.corporation != self.corporation:
				return BuyShareOrder.FIRST_COST * self.corporation.assets
			else:
				return BuyShareOrder.FIRST_AND_CITIZEN_COST * self.corporation.assets
		else:
			return BuyShareOrder.BASE_COST * self.corporation.assets

	def resolve(self):
		# Pay.
		self.player.money -= self.get_cost()
		self.player.save()

		# Add a share to the player
		Share(
			corporation=self.corporation,
			player=self.player
		).save()

		# Create game_event
		self.player.game.add_event(event_type=Game.BUY_SHARE, data={"player": self.player.name, "corporation": self.corporation.base_corporation.name}, corporation=self.corporation, players=[self.player])

	def description(self):
		return u"Acheter une part de la corporation %s (actifs actuels : %s)" % (self.corporation.base_corporation.name, self.corporation.assets)

	def get_form(self, data=None):
		form = super(BuyShareOrder, self).get_form(data)
		form.fields['corporation'].queryset = self.player.game.corporation_set.all()

		return form

orders = (BuyShareOrder,)
