# -*- coding: utf-8 -*-
from engine.tasks import OrderResolutionTask
from engine_modules.market.models import CorporationMarket
from engine_modules.market_bubbles.models import MarketBubble
from engine_modules.corporation.models import Corporation

class UpdateMarketBubblesTask(OrderResolutionTask):
	"""
	Recalculate Market bubbles for every market
	"""

	RESOLUTION_ORDER = 500

	def run(self, game):

		# We can force the use of bubbles  using the force_invisible_hand flag
                if game.disable_side_effects and not hasattr(game, 'force_bubbles'):
                        return

		# First, we have to reset every corporation's assets_modifier
		corporations = Corporation.objects.filter(game=game)
		modifiers = {}
		for corporation in corporations:
			modifiers[corporation] = 0

		corporation_markets = CorporationMarket.objects.filter(corporation__game=game).order_by('market', '-value')

#		print "Corporation Markets:"
#		print corporation_markets

		# build a dict: market name -> list of (Corporation, Assests in market)
		# this means we parse the list twice, but no requests, so it should not impact performance, and it is clearer
		markets = {}
		for corporation_market in corporation_markets:
			if corporation_market.market not in markets.keys():
				markets[corporation_market.market] = []

			# 'append' will preserve the order
			markets[corporation_market.market].append((corporation_market.corporation, corporation_market.value))

		for market in markets.keys():
			# should be ordered from min value to max value
			max_value = markets[market][-1][1]
			for (corporation, value) in markets[market]:
				if value == 0:
					modifiers[corporation] -= 1
					bubble = MarketBubble(corporation=corporation, market=market, turn=game.current_turn, value=-1)
					bubble.save()

				elif len(markets[market]) == 1:
					modifiers[corporation] += 1
					bubble = MarketBubble(corporation=corporation, market=market, turn=game.current_turn, value=1)
					bubble.save()

				elif value == max_value:
					if corporation == markets[market][0][0] and markets[market][1][1] < value:
						# this corporation is the only one with max_value
						modifiers[corporation] += 1
						bubble = MarketBubble(corporation=corporation, market=market, turn=game.current_turn, value=1)
						bubble.save()

		for corporation in corporations:
			corporation.assets_modifier = modifiers[corporation]
			corporation.save()

tasks = (UpdateMarketBubblesTask, )
