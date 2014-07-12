from engine.tasks import OrderResolutionTask
from engine_modules.speculation.models import CorporationSpeculationOrder


class CorporationSpeculationTask(OrderResolutionTask):
	"""
	Resolve corporations speculations
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = CorporationSpeculationOrder


tasks = (CorporationSpeculationTask, )
