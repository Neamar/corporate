from engine.tasks import ResolutionTask
from engine_modules.influence.orders import BuyInfluenceOrder


class BuyInfluenceTask(ResolutionTask):
	"""
	Buy new Influence level
	"""
	priority = 90

	def run(self, game):
		"""
		Retrieve all BuyInfluenceOrder
		"""
		BuyInfluenceOrder.objects.filter(player__game=game, turn=game.current_turn)



tasks = (BuyInfluenceTask,)
