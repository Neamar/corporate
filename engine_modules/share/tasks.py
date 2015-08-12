# -*- coding: utf-8 -*-
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
	# To avoid double penalty and to simplfy the game, we removed last bonus
	LAST_BONUS = 1

	RESOLUTION_ORDER = 800

	def run(self, game):
		"""
		Retrieve all Share from all players
		"""
		all_shares = Share.objects.filter(player__game=game).select_related('corporation')

		shares = {}

		# Group shares by corporation and players
		for share in all_shares:
			# Reduce to keep non duplicate only
			key = (share.corporation_id, share.player_id)
			if key in shares:
				shares[key].count += 1
			else:
				shares[key] = share
				share.count = 1

		ladder = game.get_ladder()

		for share in shares.values():
			dividend = share.count * self.SHARE_BASE_VALUE * share.corporation.assets

			if share.corporation == ladder[0]:
				dividend *= self.FIRST_BONUS
			if share.corporation == ladder[-1]:
				dividend *= self.LAST_BONUS

			# If the corporation hasn't crashed. We test it here because the corporation really collapse at resoltuion_order 1000. At this time, asset may be negative
			if dividend > 0:
				dividend = int(dividend)
				share.player.money += dividend
				share.player.save()

tasks = (BuyShareTask, DividendTask)
