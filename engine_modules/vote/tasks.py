from engine.tasks import OrderResolutionTask
from engine_modules.vote.models import VoteOrder


class VoteTask(OrderResolutionTask):
	"""
	Buy new Influence level
	"""
	RESOLUTION_ORDER = 100
	ORDER_TYPE = VoteOrder

tasks = (VoteTask, )
