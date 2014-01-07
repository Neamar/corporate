from engine.tasks import OrderResolutionTask
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder
from random import shuffle

class OffensiveRunTask(OrderResolutionTask):
	"""
	A Task to resolve all Offensive Runs (DataSteal and Sabotage)
	"""	
	resolution_order = 350
	ORDER_TYPES = [DataStealOrder, SabotageOrder]

	def run(self, game):
		orders = []
		for order_type in self.ORDER_TYPES:
			orders += order_type.objects.filter(player__game=game, turn=game.current_turn)
		# Mix DataSteals and Sabotages
		shuffle(orders)
		# Offensive Runs should be resolved in decreasing order of success probability
		orders = sorted(orders, key=lambda order: order.get_success_probability(), reverse=True)

		for order in orders:
			order.resolve()

tasks = (OffensiveRunTask, )
