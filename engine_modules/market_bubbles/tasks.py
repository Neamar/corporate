# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

from engine.tasks import OrderResolutionTask
from engine_modules.market.models import CorporationMarket
from engine_modules.market_bubbles.models import MarketBubble
from engine_modules.corporation.models import Corporation

def reset_local_assets_modifier(corporations):
	"""
	Build a dict: corporation -> 0
	"""
	modifiers = {}
	for corporation in corporations:
		modifiers[corporation] = 0
	return modifiers

def get_market_dictionary(corporation_markets):
	"""
	Build a dict: market -> list of (Corporation, Assests in market)
	"""
	# We have to sort the corporation_markets by market from lowest to highest value
	# This has probably been done by the request, but it is external now
	markets_dict = {}
	sorted_markets = {}
	for corporation_market in corporation_markets:
		market = corporation_market.market
		if market not in sorted_markets.keys():
			sorted_markets[market] = []
			markets_dict[market] = []
			
		sorted_markets[market].append((corporation_market.corporation, corporation_market.value))

	for market in sorted_markets.keys():
		sorted_markets[market].sort(key=lambda t:t[1])
		# 'append' will preserve the order
		markets_dict[market].extend(sorted_markets[market])
	return markets_dict

def get_bubble_dictionary(corporation_markets, market_bubbles):
	"""
	Build a dict: market -> list of Bubbles starting with positive or None, then negatives or None)
	"""
	bubbles = {}
	for corporation_market in corporation_markets:
		market = corporation_market.market
		bubbles[market] = []
		for bubble in market_bubbles:
			if bubble.market == market:
				if bubble.value == 1:
					bubbles[market].insert(0, bubble)
				else:
					bubbles[market].append(bubble)

		if len(bubbles[market]) == 0:
			bubbles[market].append(None)
			bubbles[market].append(None)
		else:
			if bubbles[market][0].value == -1:
				# There was no positive bubble, but we need a placeholder
				bubbles[market].insert(0, None)
			else:
				if len(bubbles) == 1:
					# There were no negative bubbles, but we need a placeholder
					bubbles[market].append(None)
class UpdateMarketBubblesTask(OrderResolutionTask):
	"""
	Recalculate Market bubbles for every market
	"""

	RESOLUTION_ORDER = 500

	def run(self, game):

		# We can force the use of bubbles  using the force_bubbles flag
		if game.disable_side_effects and not hasattr(game, 'force_bubbles'):
			return

		corporations = Corporation.objects.filter(game=game)
		corporation_markets = CorporationMarket.objects.filter(corporation__game=game).order_by('market', '-value')

		modifiers = reset_local_assets_modifier(corporations)
		markets = get_market_dictionary(corporation_markets)
		
		for market in markets.keys():
			# should be ordered from min value to max value
			max_value = markets[market][-1][1]
			for (corporation, value) in markets[market]:
				if value <= 0:
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

class UpdateMarketBubblesAfterEffectsTask(UpdateMarketBubblesTask):
	"""
        Recalculate Market bubbles for every market
        """

        RESOLUTION_ORDER = 650

	def run(self, game):

		# We can force the use of bubbles using the force_bubbles flag
		if game.disable_side_effects and not hasattr(game, 'force_bubbles'):
			return

		corporations = Corporation.objects.filter(game=game)
		corporation_markets = CorporationMarket.objects.filter(corporation__game=game).order_by('market', '-value')
		market_bubbles = MarketBubble.objects.filter(corporation__game=game, turn=game.current_turn)

		modifiers = reset_local_assets_modifier(corporations)
		markets = get_market_dictionary(corporation_markets)
		bubbles = get_bubble_dictionary(corporation_markets, market_bubbles)

		for market in markets.keys():
			# should be ordered from min value to max value
			max_value = markets[market][-1][1]
			if max_value > 0:
				if len(markets[market]) == 1:
					pass
					
			for (corporation, value) in markets[market]:
				
				negative_bubble = None
				try:
					# This might be making 2 DB requests when 1 could suffice, but I believe it makes the code much clearer
					negative_bubble = MarketBubble.objects.get(corporation=corporation, market=market, turn=game.current_turn, value=-1)
				except ObjectDoesNotExist:
					if value <= 0:
						modifiers[corporation] -= 1
						bubble = MarketBubble(corporation=corporation, market=market, turn=game.current_turn, value=-1)
						bubble.save()
				if value > 0:
					if negative_bubble is not None:
						negative_bubble.delete()
					#positive_bubble = MarketBubble.objects.get(corporation=corporation, market=market, turn=game.current_turn, value=1)
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
		
tasks = (UpdateMarketBubblesTask, UpdateMarketBubblesAfterEffectsTask)
