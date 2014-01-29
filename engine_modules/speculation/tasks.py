from engine.tasks import OrderResolutionTask
from engine_modules.speculation.models import CorporationSpeculationOrder


class CorporationSpeculationTask(OrderResolutionTask):
	"""
	Speculate on a corporation's rank
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = CorporationSpeculationOrder


tasks = (CorporationSpeculationTask,)