from engine.tasks import OrderResolutionTask
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder

class DataStealTask(OrderResolutionTask):
	"""
	Order an information robbery on a corporation
	"""	
	resolution_order = 350
	ORDER_TYPE = DataStealOrder

class ProtectionTask(OrderResolutionTask):
	"""
	Protect a corporation against nefarious actions
	"""
	resolution_order = 300
	ORDER_TYPE = ProtectionOrder

class SabotageTask(OrderResolutionTask):
	"""
	Hinder the progress of a corporation
	"""
	resolution_order = 350
	ORDER_TYPE = SabotageOrder

tasks = (DataStealTask, ProtectionTask, SabotageTask, )
