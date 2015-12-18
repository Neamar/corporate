from engine.tasks import OrderResolutionTask
from engine_modules.corporation_run.models import DataStealOrder, SabotageOrder, ProtectionOrder, ExtractionOrder
from engine_modules.market.models import CorporationMarket


class OffensiveRunTask(OrderResolutionTask):
	"""
	Resolve Offensive corporations runs (DataSteal, Sabotage, Extraction)
	"""
	RESOLUTION_ORDER = 350
	ORDER_TYPES = [DataStealOrder, SabotageOrder, ExtractionOrder]

	def run(self, game):
		orders = []
		# For every type of order, we run each order by raw_probability desc on each corporationmarket until one of them is sucessful
		# Once at least one is successful, the others fail
		for corporationmarket in CorporationMarket.objects.filter(turn=game.current_turn, corporation__game=game, corporation__crash_turn__isnull=True):
			for order_type in self.ORDER_TYPES:
				orders = order_type.objects.filter(player__game=game, turn=game.current_turn, target_corporation_market=corporationmarket)
				sorted_orders = sorted(orders, key=lambda order: order.get_raw_probability(), reverse=True)
				next_run_failed = False
				for order in sorted_orders:
					if next_run_failed:
						order.resolve_to_fail()
					elif order.resolve():
						next_run_failed = True


class ProtectionRunTask(OrderResolutionTask):
	"""
	Debit Protection runs from players
	"""
	RESOLUTION_ORDER = 349
	ORDER_TYPE = ProtectionOrder

	def run(self, game):
		orders = self.ORDER_TYPE.objects.filter(player__game=game, turn=game.current_turn)
		for order in orders:
			order.resolve()

tasks = (OffensiveRunTask, ProtectionRunTask)
