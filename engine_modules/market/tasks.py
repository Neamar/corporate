# -*- coding: utf-8 -*-
from django.db.models import Max

from engine.tasks import ResolutionTask
from engine_modules.market.models import CorporationMarket


class UpdateBubblesTask(ResolutionTask):
	"""
	Update the bubble value on the CorporationMarket objects
	"""
	RESOLUTION_ORDER = 500

	def run(self, game):
		# We can force the use of bubbles  using the force_bubbles flag

		# I do NOT remember why the test was "not hasattr(game, 'force_bubbles')", I left it here just in case
		# but the check == False is necessary. TODO: check if 'hasattr' has meaning (-> can a game not have an attribute 'force_bubbles' ?)
		if game.disable_side_effects and (not hasattr(game, 'force_bubbles') or not game.force_bubbles):
			return

		corporation_markets = CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn).annotate(maxval=Max('value')).order_by('market__name', '-value')
		modifiers = {}
		markets_blacklist = []
		for i in range(len(corporation_markets)):
			cm = corporation_markets[i]
			if cm.corporation not in modifiers.keys():
				modifiers[cm.corporation] = 0
			if cm.market not in markets_blacklist:
				if cm.value == 0:
					# Negative bubble
					cm.bubble_value = -1
					cm.save()
					# We have to propagate the modification to the corporation's assets_modifier
					modifiers[cm.corporation] += cm.bubble_value
				# This 'elif' may appear innocuous, but by no means is it so: it signifies that a CorporationMarket with a value at 0 is NOT eligible
				# to a dominaion bubble, even if other Corporations were to have even lower assets on this Market.
				# This might seem redundant because Markets are not supposed to have negative values, but if taht changes (unlikely), this'll be ready.
				# In any case, tha means '0' CANNOT be a superposed state for 'bubble_value', so we don't need 2 fields (for positive and negative bubbles)
				elif cm.value == cm.maxval:
					if (i == len(corporation_markets) - 1) or (corporation_markets[i + 1].market != cm.market) or (corporation_markets[i + 1].value < cm.value):
						cm.bubble_value = 1
						cm.save()
						# We have to propagate the modification to the corporation's assets_modifier
						modifiers[cm.corporation] += cm.bubble_value
					else:
						# There can be no domination bubble on this market
						markets_blacklist.append(cm.market)
						
		for corporation in modifiers.keys():
			corporation.update_modifier(modifiers[corporation])
			corporation.save()


class UpdateBubblesAfterEffectsTask(ResolutionTask):
	"""
	Update the bubble value on the CorporationMarket objects after the First/Last effects have been applied
	"""
	# Be careful: this task must be resolved before ReplicateCorporationMarketTask
	RESOLUTION_ORDER = 650

	def run(self, game):

		# We can force the use of bubbles  using the force_bubbles flag
		if game.disable_side_effects and not hasattr(game, 'force_bubbles') or not game.force_bubbles:
			return

		# 'bubble_value=0' is a legitimate condition, because '0' cannot result of a superposition of 1 and -1 bubbles (see UpdataBubblesTask)
		# We'll delete elements from this list that also exist this turn until we are left with only the bubbles that burst on this turn
		previous_bubble_corporation_markets = CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn - 1).exclude(bubble_value=0)
		corporation_markets = CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn).annotate(maxval=Max('value')).order_by('market__name', '-value')
		modifiers = {}
		markets_blacklist = []
		for i in range(len(corporation_markets)):
			cm = corporation_markets[i]
			if cm.corporation not in modifiers.keys():
				modifiers[cm.corporation] = 0
			if cm.market not in markets_blacklist:
				if cm.value == 0:
					# Negative bubble
					cm.bubble_value = -1
					cm.save()
					# We have to propagate the modification to the corporation's assets_modifier
					modifiers[cm.corporation] += cm.bubble_value

					for pcm in previous_bubble_corporation_markets:
						if cm.corporation == pcm.corporation and pcm.market == cm.market and pcm.value == cm.value:
							# The bubble was already here last turn, delete it from the list of possible new bubble candidates
							previous_bubble_corporation_markets.remove(pcm)
							break
					else:
						# This bubble did not exist last turn, log its creation
						game.add_event(event_type=game.GAIN_DRY_BUBBLE, data={"market": cm.market.name, "corporation": cm.corporation.base_corporation.name}, corporation=cm.corporation, corporationmarket=cm)
						
				elif cm.value == cm.maxval:
					if (i == len(corporation_markets) - 1) or (corporation_markets[i + 1].market != cm.market) or (corporation_markets[i + 1].value < cm.value):
						cm.bubble_value = 1
						cm.save()
						# We have to propagate the modification to the corporation's assets_modifier
						modifiers[cm.corporation] += cm.bubble_value

						for pcm in previous_bubble_corporation_markets:
							if cm.corporation == pcm.corporation and pcm.market == cm.market and pcm.value == cm.value:
								# The bubble was already here last turn, delete it from the list of possible new bubble candidates
								previous_bubble_corporation_markets.remove(pcm)
								break
						else:
							# This bubble did not exist last turn, log its creation
							game.add_event(event_type=game.GAIN_DOMINATION_BUBBLE, data={"market": cm.market.name, "corporation": cm.corporation.base_corporation.name}, corporation=cm.corporation, corporationmarket=cm)
						
					else:
						# There can be no domination bubble on this market
						markets_blacklist.append(cm.market)
						
		for corporation in modifiers.keys():
			corporation.update_modifier(modifiers[corporation])
			corporation.save()

		# We still have to log the deletion of the bubbles that burst
		for cm in previous_bubble_corporation_markets:
			event_type = game.LOSE_DOMINATION_BUBBLE if cm.bubble_value == 1 else game.LOSE_DRY_BUBBLE
			game.add_event(event_type=event_type, data={"market": cm.market.name, "corporation": cm.corporation.base_corporation.name}, corporation=cm.corporation, corporationmarket=cm)


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
				value=corporation_market.value,
				bubble_value=corporation_market.bubble_value)
			new_corporation_markets.append(new_corporation_market)
		# On next turn, these will be modified until they stand for the final values
		CorporationMarket.objects.bulk_create(new_corporation_markets)

tasks = (UpdateBubblesTask, UpdateBubblesAfterEffectsTask, ReplicateCorporationMarketsTask, )
