from engine.tasks import ResolutionTask
from engine_modules.influence.models import BuyInfluenceOrder


class BuyInfluenceTask(ResolutionTask):
	"""
	Buy new Influence level
	"""
	priority = 90

	def run(self, game):
		"""
		Retrieve all BuyInfluenceOrder
		"""
		pass


__tasks__ = (BuyInfluenceTask,)
