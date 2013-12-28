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


orders = (BuyShareOrder,)
