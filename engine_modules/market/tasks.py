# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from engine_modules.market.models import CorporationMarket


class ReplicateCorporationMarketsTask(ResolutionTask):
	"""
	Copy the CorporationMarket objects from current turn for next turn
	"""
	RESOLUTION_ORDER = 659
	
	def run(self, game):

		# On next turn, these will stand for the beginning values
		corporation_markets = CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn)
		new_corporation_markets = []
		for corporation_market in corporation_markets:
			new_corporation_market = CorporationMarket(
				corporation=corporation_market.corporation,
				market=corporation_market.market,
				turn=game.current_turn + 1,
				value=corporation_market.value)
			new_corporation_markets.append(new_corporation_market)
		# On next turn, these will be modified until they stand for the final values
		CorporationMarket.objects.bulk_create(new_corporation_markets)

tasks = (ReplicateCorporationMarketsTask, )
