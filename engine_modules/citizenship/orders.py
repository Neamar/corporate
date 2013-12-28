from django.db import models
from engine.models import Order
from engine_modules.corporation.models import Corporation

class CitizenShipOrder(Order):
	"""
	Order to become citizen from a new corporation
	"""
	corporation = models.ForeignKey(Corporation)

	def resolve(self):
		self.player.citizenship.corporation = self.corporation
		self.player.save()

orders = (CitizenShipOrder,)
