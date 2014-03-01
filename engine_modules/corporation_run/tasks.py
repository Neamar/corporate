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
		for order_type in self.ORDER_TYPES:
			orders += order_type.objects.filter(player__game=game, turn=game.current_turn)

		for order in orders:
			order.resolve()


class ProtectionRunTask(OrderResolutionTask):
	"""
	Debit Protection runs from players
	"""
	RESOLUTION_ORDER = 349
	ORDER_TYPE = ProtectionOrder

tasks = (OffensiveRunTask, ProtectionRunTask)
