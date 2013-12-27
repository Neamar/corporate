from engine.tasks import ResolutionTask
from engine_modules.influence.share import BuyShareOrder


class BuyShareTask(ResolutionTask):
	"""
	Buy new Influence level
	"""
	priority = 0

	def run(self, game):
		"""
		Retrieve all BuyShareOrder and resolve them
		"""
		buy_share_orders = BuyShareOrder.objects.filter(player__game=game, turn=game.current_turn)

		for buy_share_order in buy_share_orders:
			buy_share_order.resolve()			



tasks = (BuyShareTask,)
