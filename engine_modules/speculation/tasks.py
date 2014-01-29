from engine.tasks import OrderResolutionTask
from engine_modules.speculation.models import CorporationSpeculationOrder, DerivativeSpeculationOrder


class CorporationSpeculationTask(OrderResolutionTask):
	"""
	Speculate on a corporation's rank
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = CorporationSpeculationOrder

class DerivativeSpeculationTask(OrderResolutionTask):
	"""
	Speculate on a corporation's rank
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = DerivativeSpeculationOrder


tasks = (CorporationSpeculationTask, DerivativeSpeculationTask)