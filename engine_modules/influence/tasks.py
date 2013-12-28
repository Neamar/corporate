from engine.tasks import OrderResolutionTask
from engine_modules.influence.models import BuyInfluenceOrder


class BuyInfluenceTask(OrderResolutionTask):
	"""
	Buy new Influence level
	"""
	resolution_order = 900
	ORDER_TYPE = BuyInfluenceOrder



tasks = (BuyInfluenceTask,)
