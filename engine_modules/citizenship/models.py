from django.db import models
from engine.models import Player, Order
from engine_modules.corporation.models import Corporation

class CitizenShip(models.Model):
	player = models.OneToOneField(Player)
	corporation = models.ForeignKey(Corporation, null=True)


class CitizenShipOrder(Order):
	"""
	Order to become citizen from a new corporation
	"""
	corporation = models.ForeignKey(Corporation)

	def resolve(self):
		self.player.citizenship.corporation = self.corporation
		self.player.citizenship.save()

orders = (CitizenShipOrder,)
