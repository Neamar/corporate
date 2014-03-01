from engine.tasks import OrderResolutionTask
from engine_modules.speculation.models import CorporationSpeculationOrder, DerivativeSpeculationOrder


class CorporationSpeculationTask(OrderResolutionTask):
	"""
	Resolve corporations speculations
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = CorporationSpeculationOrder


class DerivativeSpeculationTask(OrderResolutionTask):
	"""
	Resolve derivatives speculations
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = DerivativeSpeculationOrder


tasks = (CorporationSpeculationTask, DerivativeSpeculationTask)
