# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask, OrderResolutionTask
from engine_modules.share.models import Share, BuyShareOrder
from messaging.models import Note


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
		"""
		all_shares = Share.objects.filter(player__game=game).select_related('corporation')

		shares = {}

		# Group shares by corporation and players
		for share in all_shares:
			# Reduce to keep non duplicate only
			key = "%s,%s" % (share.corporation_id, share.player_id)
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

			share.player.money += int(dividend)
			share.player.save()

			if share.count == 1:
				content = u"Votre part dans %s vous rapporte %s k¥" % (share.corporation.base_corporation.name, dividend)
			else:
				content = u"Vos %s parts dans %s vous rapportent %s k¥" % (share.count, share.corporation.base_corporation.name, dividend)
			share.player.add_note(category=Note.DIVIDEND, content=content)

tasks = (BuyShareTask, DividendTask)
