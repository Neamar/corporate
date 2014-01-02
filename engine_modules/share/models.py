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
	BASE_COST = 50

	corporation = models.ForeignKey(Corporation)

	def get_cost(self):
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
		title=u"Parts"
		nb_shares=self.player.share_set.filter(corporation=self.corporation).count()
		if nb_shares==1:
		  content=u"Vous avez achetés votre première part dans la corporation %s." % self.corporation.base_corporation.name
		else:
			content=u"Vous avez achetés votre %ieme part dans la corporation %s." %(nb_shares, self.corporation)
		self.player.add_note(title=title, content=content)

	def description(self):
		return u"Acheter une part de la corporation %s (actifs actuels : %s)" % (self.corporation.base_corporation.name, self.corporation.assets)


orders = (BuyShareOrder,)
