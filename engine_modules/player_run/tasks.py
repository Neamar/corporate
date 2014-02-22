# -*- coding: utf-8 -*-
from engine.tasks import OrderResolutionTask
from engine_modules.player_run.models import InformationOrder


class InformationRunTask(OrderResolutionTask):
	"""
	Resolve information runs
	"""
	RESOLUTION_ORDER = 350
	ORDER_TYPE = InformationOrder

tasks = (InformationRunTask,)
