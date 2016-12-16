from engine.tasks import OrderResolutionTask
from engine_modules.corporation_run.models import DataStealOrder, SabotageOrder, ProtectionOrder, ExtractionOrder
from engine_modules.detroit_inc.models import DIncVoteOrder
from engine_modules.market.models import CorporationMarket
from engine.models import Order


class OffensiveRunTask(OrderResolutionTask):
	"""
	Resolve Offensive corporations runs (DataSteal, Sabotage, Extraction)
	"""
	RESOLUTION_ORDER = 700
	ORDER_TYPES = [DataStealOrder, SabotageOrder, ExtractionOrder]

	def run(self, game):
		orders = []
		# We start by managing the dinc negative effect of RSEC : one random run fail before test. We don't care about the last turn :
		# There are no resolution turn after it takes place
		failed_orders = []
		if game.get_dinc_coalition(turn=game.current_turn) == DIncVoteOrder.RSEC:
			for player in game.player_set.all():
				if player.get_last_dinc_coalition() == DIncVoteOrder.CONS:
					orders = Order.objects.filter(player__game=game, turn=game.current_turn, type__in=['DataStealOrder', 'SabotageOrder', 'ExtractionOrder']).order_by('?')
					failed_orders.append(orders[0].pk)

		# For every type of order, we run each order by raw_probability desc on each corporationmarket until one of them is sucessful
		# Once at least one is successful, the others fail
		for corporationmarket in CorporationMarket.objects.filter(turn=game.current_turn, corporation__game=game, corporation__crash_turn__isnull=True):
			for order_type in self.ORDER_TYPES:
				orders = order_type.objects.filter(player__game=game, turn=game.current_turn, target_corporation_market=corporationmarket)
				sorted_orders = sorted(orders, key=lambda order: order.get_raw_probability(), reverse=True)
				next_run_failed = False
				for order in sorted_orders:
					if next_run_failed or order.pk in failed_orders:
						order.resolve_to_fail()
					elif order.resolve():
						next_run_failed = True


class ProtectionRunTask(OrderResolutionTask):
	"""
	Debit Protection runs from players
	"""
	RESOLUTION_ORDER = 600
	ORDER_TYPE = ProtectionOrder

	def run(self, game):
		orders = self.ORDER_TYPE.objects.filter(player__game=game, turn=game.current_turn)
		for order in orders:
			order.resolve()

tasks = (OffensiveRunTask, ProtectionRunTask)
