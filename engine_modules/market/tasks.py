# -*- coding: utf-8 -*-
from django.db.models import Max

from engine.tasks import ResolutionTask
from engine_modules.market.models import Market, CorporationMarket


class AbstractBubblesTask(ResolutionTask):
	"""
	This is an abstract class for the updating of Bubbles, it should be inherited from, but not used
	"""

	def run(self, game, after_effects=False):

		# We can force the use of bubbles  using the force_bubbles flag
		if game.disable_side_effects and not hasattr(game, 'force_bubbles'):
			return

		# This uses an underlying assumption: that a CorporationMarket with a value at 0 is NOT eligible to a domination bubble,
		# even if other Corporations were to have even lower assets on this Market.
		# It means '0' CANNOT be a superposed state for 'bubble_value', so we don't need 2 fields (for positive and negative bubbles)

		# We let negative bubbles on corporations crashed this turn

		# Now get all positive bubbles. We annotate the CorporationMarkets with the field 'maxval', containing the maximal value across all
		positive_bubbles = {}
		max_vals = {}
		for market in Market.objects.all():
			# A crashed corporation does not compete for positive bubble
			max_vals[market.name] = CorporationMarket.objects.filter(corporation__game=game, corporation__crash_turn__isnull=True, turn=game.current_turn, market=market).exclude(value__lte=0).aggregate(maximum=Max('value'))['maximum']
			if max_vals[market.name] is not None:
				try:
					# A crashed corporation does not compete for positive bubble
					positive_bubbles[market.name] = CorporationMarket.objects.get(corporation__game=game, corporation__crash_turn__isnull=True, turn=game.current_turn, market=market, value=max_vals[market.name])
				except:
					# There were several corporations tied for first
					pass
		previous_positive_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, bubble_value=1))

		# We find the positive bubbles that will stay
		common_old_and_new_positive_bubble = []
		for pb in positive_bubbles.values():
			for ppb in previous_positive_bubbles:
				if (ppb.corporation == pb.corporation) and (ppb.market == pb.market):
					# We add the key
					common_old_and_new_positive_bubble.append("%s%s" % (pb.corporation, pb.market))

		# We remove the old positive bubble
		for ppb in previous_positive_bubbles:
			if ppb.value <= 0 or "%s%s" % (ppb.corporation, ppb.market) not in common_old_and_new_positive_bubble:
				ppb.update_bubble(CorporationMarket.NO_BUBBLE)

		previous_negative_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, bubble_value=-1))
		negative_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, value__lte=0))
		
		# We still have to handle the previous negative bubbles
		for pnb in previous_negative_bubbles:
			if pnb.value > 0:
				# We handled the other cases in the negative_bubbles loop or we will handle it in the positive_bubble loop
				pnb.update_bubble(CorporationMarket.NO_BUBBLE)

		# We add negative bubbles on corporation which doesn't already have one
		for nb in negative_bubbles:
			if nb.bubble_value != CorporationMarket.NEGATIVE_BUBBLE:
				nb.update_bubble(CorporationMarket.NEGATIVE_BUBBLE)

		# We add the new postitive bubbles if it's a new bubble and if this market doesn't have a negative bubble
		for pb in positive_bubbles.values():
			if pb.value > 0 and "%s%s" % (pb.corporation, pb.market) not in common_old_and_new_positive_bubble:
				pb.update_bubble(CorporationMarket.DOMINATION_BUBBLE)


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
	RESOLUTION_ORDER = 650

	def run(self, game):

		if not hasattr(game, 'disable_bubble_reevaluation'):
			super(UpdateBubblesAfterEffectsTask, self).run(game, after_effects=True)
		return


class UpdateBubblesAfterCrashTask(AbstractBubblesTask):
	"""
	Update the bubble value on the CorporationMarket objects after the Crash effects have been applied
	"""
	# Be careful: this task must be resolved before ReplicateCorporationMarketTask
	RESOLUTION_ORDER = 860

	def run(self, game):

		if not hasattr(game, 'disable_bubble_reevaluation'):
			super(UpdateBubblesAfterCrashTask, self).run(game, after_effects=True)

		# We build the logs. We need to calculate the difference bewtween the end on last turn and now to create events
		# We don't do it in AbstractBubblesTask because we don't want to sent the temporaty states.

		# We let negative bubbles on corporations crashed this turn
		negative_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, bubble_value=-1))
		previous_negative_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn - 1, bubble_value=-1))
		positive_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, bubble_value=1))
		previous_positive_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn - 1, bubble_value=1))

		for nb in negative_bubbles:
			for pnb in previous_negative_bubbles:
				if (pnb.corporation == nb.corporation) and (pnb.market == nb.market):
					# This is not a new bubble
					break
			else:
				game.add_event(event_type=game.GAIN_NEGATIVE_BUBBLE, data={"market": nb.market.name, "corporation": nb.corporation.base_corporation.name}, delta=-1, corporation=nb.corporation)

		for pnb in previous_negative_bubbles:
			for nb in negative_bubbles:
				if (pnb.corporation == nb.corporation) and (pnb.market == nb.market):
					# This is not a new bubble
					break
			else:
				game.add_event(event_type=game.LOSE_NEGATIVE_BUBBLE, data={"market": pnb.market.name, "corporation": pnb.corporation.base_corporation.name}, delta=1, corporation=pnb.corporation)

		for pb in positive_bubbles:
			for ppb in previous_positive_bubbles:
				if (ppb.corporation == pb.corporation) and (ppb.market == pb.market):
					# This is not a new bubble
					break
			else:
				game.add_event(event_type=game.GAIN_DOMINATION_BUBBLE, data={"market": pb.market.name, "corporation": pb.corporation.base_corporation.name}, delta=1, corporation=pb.corporation)

		for ppb in previous_positive_bubbles:
			for pb in positive_bubbles:
				if (ppb.corporation == pb.corporation) and (ppb.market == pb.market):
					# This is not a new bubble
					break
			else:
				game.add_event(event_type=game.LOSE_DOMINATION_BUBBLE, data={"market": ppb.market.name, "corporation": ppb.corporation.base_corporation.name}, delta=-1, corporation=ppb.corporation)

		return


class CreateBubblesAfterGameCreationTask(AbstractBubblesTask):
	"""
	Update the bubble value on the CorporationMarket objects after the Crash effects have been applied
	"""
	# Be careful: this task must be resolved before ReplicateCorporationMarketTask
	RESOLUTION_ORDER = 100

	def run(self, game):
		if not hasattr(game, 'disable_bubble_reevaluation'):
			super(CreateBubblesAfterGameCreationTask, self).run(game, after_effects=True)


class ReplicateCorporationMarketsTask(ResolutionTask):
	"""
	Copy the CorporationMarket objects from current turn for next turn
	"""
	RESOLUTION_ORDER = 870
	
	def run(self, game):

		# On next turn, these will stand for the beginning values
		corporation_markets = CorporationMarket.objects.filter(corporation__game=game, corporation__crash_turn__isnull=True, turn=game.current_turn)
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

tasks = (UpdateBubblesTask, UpdateBubblesAfterEffectsTask, UpdateBubblesAfterCrashTask, ReplicateCorporationMarketsTask, )

initialisation_tasks = (CreateBubblesAfterGameCreationTask, ReplicateCorporationMarketsTask, )
