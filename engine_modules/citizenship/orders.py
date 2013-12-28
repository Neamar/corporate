from django.db import models
from engine.models import Order
from engine_modules.corporation.models import Corporation

class CitizenShipOrder(Order):
	"""
	Order to be a Citizen
	"""
	corporation = models.ForeignKey(Corporation)


orders = (CitizenShipOrder,)