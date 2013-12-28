from engine.tasks import OrderResolutionTask
from engine_modules.influence.models import BuyInfluenceOrder


class BuyInfluenceTask(OrderResolutionTask):
	"""
	Buy new Influence level
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = BuyInfluenceOrder



tasks = (BuyInfluenceTask,)
