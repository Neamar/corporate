from engine.tasks import OrderResolutionTask
from engine_modules.corporation_run.models import DataStealOrder, SabotageOrder, ProtectionOrder
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
		# Mix DataSteals and Sabotages for random order resolution on same percentage
		shuffle(orders)
		# Offensive Runs should be resolved in decreasing order of success probability
		orders = sorted(orders, key=lambda order: order.get_success_probability(), reverse=True)

		for order in orders:
			order.resolve()

class ProtectionRunPaymentTask(OrderResolutionTask):
	"""
	A Task to deduce costs of Protection Runs
	"""	
	resolution_order = 350
	ORDER_TYPES = [ProtectionOrder]

	def run(self, game):
		orders = []
		for order_type in self.ORDER_TYPES:
			orders += order_type.objects.filter(player__game=game, turn=game.current_turn)
			
		for order in orders:
			order.player.money -= order.get_cost()
			order.player.save()

tasks = (OffensiveRunTask, ProtectionRunPaymentTask)