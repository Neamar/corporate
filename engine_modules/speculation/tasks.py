from engine.tasks import OrderResolutionTask
from engine_modules.speculation.models import SpeculationOrder


class SpeculationTask(OrderResolutionTask):
	"""
	Speculate on a corporation's rank
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = SpeculationOrder


tasks = (SpeculationTask,)