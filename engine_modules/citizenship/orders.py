from django.db import models
from engine.models import Order
from engine_modules.corporation.models import Corporation
from engine_modules.citizenship.models import CitizenShip

class CitizenShipOrder(Order):
	"""
	Order to be a Citizen
	"""
	corporation = models.ForeignKey(Corporation)

	def resolve(self):
		citizen_ship = CitizenShip(player=self.player, corporation=self.corporation)
		citizen_ship.save()

orders = (CitizenShipOrder,)