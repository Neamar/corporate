from engine.tasks import OrderResolutionTask
from engine_modules.corporation_run.models import DataStealOrder, SabotageOrder, ProtectionOrder, ExtractionOrder


class OffensiveRunTask(OrderResolutionTask):
	"""
	Resolve Offensive corporations runs (DataSteal, Sabotage, Extraction)
	"""
	RESOLUTION_ORDER = 350
	ORDER_TYPES = [DataStealOrder, SabotageOrder, ExtractionOrder]

	def run(self, game):
		orders = []
		# For every type of order, we run each order order by raw_probability desc until one of them is sucessful
		for order_type in self.ORDER_TYPES:
			orders = order_type.objects.filter(player__game=game, turn=game.current_turn)
			sorted_orders = sorted(orders, key=lambda order: order.get_raw_probability(), reverse=True)
			for order in sorted_orders:
				if order.resolve():
					break


class ProtectionRunTask(OrderResolutionTask):
	"""
	Debit Protection runs from players
	"""
	RESOLUTION_ORDER = 349
	ORDER_TYPE = ProtectionOrder

tasks = (OffensiveRunTask, ProtectionRunTask)
