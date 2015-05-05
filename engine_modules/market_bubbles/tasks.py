# -*- coding: utf-8 -*-
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
	# We have to sort the corporation_markets by market from highest to lowest value
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
		sorted_markets[market].sort(key=lambda t: t[1], reverse=True)
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
				if len(bubbles[market]) == 1:
					# There were no negative bubbles, but we need a placeholder
					bubbles[market].append(None)
	return bubbles


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
		corporation_markets = CorporationMarket.objects.filter(corporation__game=game).order_by('market', 'value')

		modifiers = reset_local_assets_modifier(corporations)
		markets = get_market_dictionary(corporation_markets)
		
		for market in markets.keys():
			# should be ordered from min value to max value
			max_value = markets[market][0][1]
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
		corporation_markets = CorporationMarket.objects.filter(corporation__game=game).order_by('market', 'value')
		market_bubbles = MarketBubble.objects.filter(corporation__game=game, turn=game.current_turn)

		# Waring: in this case, the values in modifiers are relative to those already in place from the other bubbles Task
		modifiers = reset_local_assets_modifier(corporations)
		markets = get_market_dictionary(corporation_markets)
		bubbles = get_bubble_dictionary(corporation_markets, market_bubbles)

		for market in markets.keys():
			# should be ordered from min value to max value
			max_value = markets[market][0][1]
			# We have to delete the obsolete negative bubbles first, or we'll violate the unique_together("corporation", "market", "turn") constraint if we have to add a positive bubble
			domination_bubble = bubbles[market][0]
			for (corporation, value) in markets[market]:
				if bubbles[market][1] is None or corporation not in [b.corporation for b in bubbles[market][1:]]:
					if value <= 0:
						modifiers[corporation] -= 1
						# Same here, if we just add a new bubble, we'll fail the constraint
						if domination_bubble.corporation == corporation:
							bubble = domination_bubble
							modifiers[domination_bubble.corporation] -= 1
							domination_bubble = None
							bubble.value = -1
						else:
							bubble = MarketBubble(corporation=corporation, market=market, turn=game.current_turn, value=-1)
						bubble.save()
				elif value > 0:
					for b in bubbles[market][1:]:
						if b.corporation == corporation and b.value == -1:
							modifiers[corporation] += 1
							b.delete()

			if domination_bubble is not None:
				if domination_bubble.corporation != markets[market][0][0]:
					if len(markets) == 1 or markets[1][0] < max_value:
						# The corporation dominating has been changed by First/Last effects, update the bubble
						modifiers[markets[0][0]] += 1
						domination_bubble.update(corporation=markets[market][0][0])
					else:
						# First/Last effects made it so there is no longer a domination on this market, burst former domination bubble
						domination_bubble.delete()
					modifiers[domination_bubble.corporation] -= 1
			elif max_value > 0 and (len(markets[market]) == 1 or markets[market][0][1] > markets[market][1][1]):
				# There is a new domination on this market, create a bubble
				modifiers[markets[market][0][0]] += 1
				domination_bubble = MarketBubble(corporation=markets[market][0][0], market=market, turn=game.current_turn, value=1)
				domination_bubble.save()

		for corporation in corporations:
			corporation.assets_modifier += modifiers[corporation]
			corporation.save()
		
tasks = (UpdateMarketBubblesTask, UpdateMarketBubblesAfterEffectsTask)
