# -*- coding: utf-8 -*-
from engine.tasks import OrderResolutionTask
from engine_modules.citizenship.models import CitizenShipOrder


class CitizenshipTask(OrderResolutionTask):
	"""
	Update players citizenships
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = CitizenShipOrder

tasks = (CitizenshipTask,)
