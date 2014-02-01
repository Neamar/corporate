# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Player, Order
from engine_modules.corporation.models import Corporation


class Share(models.Model):
	"""
	A share held by some player
	"""
	corporation = models.ForeignKey(Corporation)
	player = models.ForeignKey(Player)
	turn = models.PositiveSmallIntegerField()


class BuyShareOrder(Order):
	"""
	Order to buy a corporation share
	"""
	BASE_COST = 100
	FIRST_COST = 125
	FIRST_AND_CITIZEN_COST = 100

	corporation = models.ForeignKey(Corporation)

	def get_cost(self):
		if self.corporation == self.player.game.get_ordered_corporations()[0]:
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

		# Send a note for final message
		category = u"Parts"
		nb_shares = self.player.share_set.filter(corporation=self.corporation).count()
		if nb_shares == 1:
		  content = u"Vous avez acheté votre première part dans %s." % self.corporation.base_corporation.name
		  global_content = u"%s a acheté sa première part dans %s." % (self.player, self.corporation.base_corporation.name)
		else:
			content = u"Vous avez acheté votre %ième part dans %s." %(nb_shares, self.corporation)
			global_content = u"%s a acheté sa %ième part dans %s." %(self.player,nb_shares, self.corporation)
		self.player.add_note(category=category, content=content)
		self.player.game.add_note(category=category, content=global_content)

	def description(self):
		return u"Acheter une part de la corporation %s (actifs actuels : %s)" % (self.corporation.base_corporation.name, self.corporation.assets)


orders = (BuyShareOrder,)
