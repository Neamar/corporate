# -*- coding: utf-8 -*-
from django.db.models import Max

from engine.tasks import ResolutionTask
from engine_modules.corporation.models import Corporation
from engine_modules.market.models import Market, CorporationMarket


class AbstractBubblesTask(ResolutionTask):
	"""
	This is an abstract class for the updating of Bubbles, it should be inherited from, but not used

	TODO : actual logging does not work. It just create logs for difference between the state before first/Last/crash effects and after first/last/crash effect.
	We must create a log function that looks between end of last turn and after first/last/crash effect. Most of the time it will be the same.
	"""

	def run(self, game, after_effects=False):

		# We can force the use of bubbles  using the force_bubbles flag
		if game.disable_side_effects and not hasattr(game, 'force_bubbles'):
			return

		# This uses an underlying assumption: that a CorporationMarket with a value at 0 is NOT eligible to a domination bubble,
		# even if other Corporations were to have even lower assets on this Market. This might seem redundant because Markets are not supposed to have negative values,
		# but if that changes (unlikely), this'll be ready. It means '0' CANNOT be a superposed state for 'bubble_value', so we don't need 2 fields (for positive and negative bubbles)
		# get all negative bubbles, in alphabetical order of the name of the Market on which they apply
		# Turn everything to list, because QuerySets don't have a 'remove' method

		# TODO : remove positive bubbles of all crashed corporations

		negative_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, value__lte=0).order_by('market__name'))
		previous_negative_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, bubble_value=-1).order_by('market__name'))

		# Now get all positive bubbles. We annotate the CorporationMarkets with the field 'maxval', containing the maximal value across all
		positive_bubbles = {}
		max_vals = {}
		for market in Market.objects.all():
			# TODO : filter on CorporationMarket with corporation not crashed (with attribute crash_turn = none). A crashed corporation can't have a positive bubble
			max_vals[market.name] = CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, market=market).exclude(value__lte=0).aggregate(maximum=Max('value'))['maximum']
			if max_vals[market.name] is not None:
				try:
					# TODO : filter on CorporationMarket with corporation not crashed (with attribute crash_turn = none). A crashed corporation can't have a positive bubble
					positive_bubbles[market.name] = CorporationMarket.objects.get(corporation__game=game, turn=game.current_turn, market=market, value=max_vals[market.name])
				except:
					# There were several corporations tied for first
					pass
		previous_positive_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, bubble_value=1))

		modifiers = {}
		for corporation in Corporation.objects.filter(game=game):
			modifiers[corporation] = 0

		for nb in negative_bubbles:
			# This test differentiates corporations descending to 0, from the ones ascending to 0. The former should get a negative bubble, the latter shouldn't,
			# because the negative bubble are an incentive to get that market back up. If you get it back up to 0, your previous bubble is erased and you don't get a new one.
			# Ascending corporations have a bubble value of -1 because they had a negative bubble last turn, the others do not
			if nb.bubble_value >= 0 or nb.value < 0:
				# The following must absolutely be executed in the 'if' and not the 'else', because although the bubbles in the 'else'
				# have been categorized as negative bubbles, they are actually popping this turn because they came back up to 0
				for pnb in previous_negative_bubbles:
					if (pnb.corporation == nb.corporation) and (pnb.market == nb.market):
						# This is not a new bubble
						previous_negative_bubbles.remove(pnb)
						break
				else:
					modifiers[nb.corporation] += nb.update_bubble(CorporationMarket.NEGATIVE_BUBBLE)
					if after_effects:
						# This bubble did not exist last turn, log its creation
						game.add_event(event_type=game.GAIN_NEGATIVE_BUBBLE, data={"market": nb.market.name, "corporation": nb.corporation.base_corporation.name}, corporation=nb.corporation, corporationmarket=nb)
			else:
				# This CorporationMarket had a negative bubble, and came back up: don't shoot the ambulance, actually, help it a bit
				# We do not have to log the bubble popping, it will be logged later, because we haven't removed it from previous_negative_bubbles
				modifiers[nb.corporation] += nb.update_bubble(CorporationMarket.NO_BUBBLE)

				# We have to check whether that corporation has a domination bubble by getting back up to 1 because a negative bubble disappeared.
				# That is only possible if the max_val for this market is None, because the query calculating it has a .exclude(value__lte=0) clause.
				# However, if the max_val value is 1, we have to remove the possible CorporationMarket in positive_bubbles, because it no longer has a domination
				if max_vals[nb.market.name] is None:
					max_vals[nb.market.name] = nb.value
					# We have to do it here, because if we do it in the previous_negative_bubbles loop, we won't have a handle on nb:
					# We'll have one on the corresponding pnb object, which will not have been updated in this loop, so the value from update_bubble will be wrong
					positive_bubbles[nb.market.name] = nb
				elif max_vals[nb.market.name] == 1 and nb.market.name in positive_bubbles.keys():
					# This corporation used to have the highest value with 1, but now there are 2 of them
					max_vals[nb.market.name] = None
					del positive_bubbles[nb.market.name]

		# We still have to handle the deletion of the bubbles that burst: We have to log them and update bubble_value
		for pnb in previous_negative_bubbles:
			if pnb.value > 0 and pnb.value != max_vals[pnb.market.name]:
				# We handled the other cases in the negative_bubbles loop or we will handle it in the positive_bubble loop
				modifiers[pnb.corporation] += pnb.update_bubble(CorporationMarket.NO_BUBBLE)
				pnb.save()

			if after_effects:
				game.add_event(event_type=game.LOSE_NEGATIVE_BUBBLE, data={"market": pnb.market.name, "corporation": pnb.corporation.base_corporation.name}, corporation=pnb.corporation, corporationmarket=pnb)

		for pb in positive_bubbles.values():
			for ppb in previous_positive_bubbles:
				if (ppb.corporation == pb.corporation) and (ppb.market == pb.market):
					# This is not a new bubble
					previous_positive_bubbles.remove(ppb)
					break
			else:
				modifiers[pb.corporation] += pb.update_bubble(CorporationMarket.DOMINATION_BUBBLE)
				if after_effects:
					# This bubble did not exist last turn, log its creation
					game.add_event(event_type=game.GAIN_DOMINATION_BUBBLE, data={"market": pb.market.name, "corporation": pb.corporation.base_corporation.name}, corporation=pb.corporation, corporationmarket=pb)

		for ppb in previous_positive_bubbles:
			if ppb.value > 0:
				# We already handled the other cases in the negative_bubble loop
				modifiers[ppb.corporation] += ppb.update_bubble(CorporationMarket.NO_BUBBLE)
				ppb.save()

			if after_effects:
				game.add_event(event_type=game.LOSE_DOMINATION_BUBBLE, data={"market": ppb.market.name, "corporation": ppb.corporation.base_corporation.name}, corporation=ppb.corporation, corporationmarket=ppb)

		for corporation in modifiers.keys():
			corporation.update_modifier(modifiers[corporation])


class UpdateBubblesTask(AbstractBubblesTask):
	"""
	Update the bubble value on the CorporationMarket objects
	"""
	RESOLUTION_ORDER = 500

	def run(self, game):

		super(UpdateBubblesTask, self).run(game, after_effects=False)
		return


class UpdateBubblesAfterEffectsTask(AbstractBubblesTask):
	"""
	Update the bubble value on the CorporationMarket objects after the First/Last effects have been applied
	"""
	# Be careful: this task must be resolved before ReplicateCorporationMarketTask
	RESOLUTION_ORDER = 650

	def run(self, game):

		if not hasattr(game, 'disable_bubble_reevaluation'):
			super(UpdateBubblesAfterEffectsTask, self).run(game, after_effects=True)
		return


class ReplicateCorporationMarketsTask(ResolutionTask):
	"""
	Copy the CorporationMarket objects from current turn for next turn
	"""
	RESOLUTION_ORDER = 659
	
	def run(self, game):

		# On next turn, these will stand for the beginning values
		# TODO : remove all the corporationMarkets form crashed corporation on the filter
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
