from engine.tasks import ResolutionTask
from engine_modules.share.orders import BuyShareOrder
from engine_modules.share.models import Share


class BuyShareTask(ResolutionTask):
	"""
	Buy new Influence level
	"""
	priority = 0

	def run(self, game):
		"""
		Retrieve all BuyShareOrder and resolve them
		TODO: factor out
		"""
		buy_share_orders = BuyShareOrder.objects.filter(player__game=game, turn=game.current_turn)

		for buy_share_order in buy_share_orders:
			buy_share_order.resolve()			


class DividendTask(ResolutionTask):
	"""
	It's time to get money!
	"""
	SHARE_BASE_VALUE = 50

	priority = 80

	def run(self, game):
		"""
		Retrieve all Share from all players
		TODO: megaoptimize queries
		"""
		shares = Share.objects.filter(player__game=game)
		ordered_corporations = game.get_ordered_corporations()

		for share in shares:
			# Dont give dividends for share bought this turn, unless we're in turn 1 or 2
			if share.turn < game.current_turn or game.current_turn < 2:
				dividend = self.SHARE_BASE_VALUE * share.corporation.assets
				if share.corporation == ordered_corporations[0]:
					dividend *= 1.25
				if share.corporation == ordered_corporations[-1]:
					dividend *= 0.75

				share.player.money += int(dividend)
				share.player.save()

tasks = (BuyShareTask, DividendTask)
