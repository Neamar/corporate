from engine.tasks import OrderResolutionTask
from engine_modules.vote.models import VoteOrder


class VoteTask(OrderResolutionTask):
	"""
	Resolve player's corporation votes
	"""
	RESOLUTION_ORDER = 100
	ORDER_TYPE = VoteOrder

tasks = (VoteTask, )
