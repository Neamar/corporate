from engine.tasks import ResolutionTask, OrderResolutionTask
from engine_modules.share.models import Share, BuyShareOrder


class BuyShareTask(OrderResolutionTask):
	"""
	Buy all shares for all players
	"""
	RESOLUTION_ORDER = 0
	ORDER_TYPE = BuyShareOrder


class DividendTask(ResolutionTask):
	"""
	It's time to get money!
	"""
	SHARE_BASE_VALUE = 50
	FIRST_BONUS = 1.5
	LAST_BONUS = 0.5

	RESOLUTION_ORDER = 800

	def run(self, game):
		"""
		Retrieve all Share from all players
		TODO: megaoptimize queries
		"""
		shares = Share.objects.filter(player__game=game)
		ladder = game.get_ordered_corporations()

		for share in shares:
			dividend = self.SHARE_BASE_VALUE * share.corporation.assets
			if share.corporation == ladder[0]:
				dividend *= self.FIRST_BONUS
			if share.corporation == ladder[-1]:
				dividend *= self.LAST_BONUS

			share.player.money += int(dividend)
			share.player.save()

tasks = (BuyShareTask, DividendTask)
