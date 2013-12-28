from engine.tasks import ResolutionTask
from engine_modules.influence.models import BuyInfluenceOrder


class BuyInfluenceTask(ResolutionTask):
	"""
	Buy new Influence level
	"""
	priority = 90

	def run(self, game):
		"""
		Retrieve all BuyInfluenceOrder and resolve them
		"""
		buy_influence_orders = BuyInfluenceOrder.objects.filter(player__game=game, turn=game.current_turn)

		for buy_influence_order in buy_influence_orders:
			buy_influence_order.resolve()			



tasks = (BuyInfluenceTask,)
