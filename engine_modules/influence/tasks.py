from engine.modules import register_module, ResolutionTask
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

register_module(
	tasks=[BuyInfluenceTask()],
	orders=[BuyInfluenceOrder],
)
