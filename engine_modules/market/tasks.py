# -*- coding: utf-8 -*-
from django.db.models import Max

from engine.tasks import ResolutionTask
from engine_modules.corporation.models import Corporation
from engine_modules.market.models import Market, CorporationMarket


class AbstractBubblesTask(ResolutionTask):
	"""
	This is an abstract class for the updating of Bubbles, it should be inherited from, but not used
	"""

	def run(self, game, after_effects=False):

		# We can force the use of bubbles  using the force_bubbles flag
		if game.disable_side_effects and not hasattr(game, 'force_bubbles'):
			return

		# DEBUG had to weasel around flake8 # corp_mark = CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn) # for cm in corp_mark:
			# print " 1 CorporationMarket: %s.%s -> %i (%i)" % (cm.corporation.base_corporation_slug, cm.market.name, cm.value, cm.bubble_value)

		# This uses an underlying assumption: that a CorporationMarket with a value at 0 is NOT eligible to a domination bubble,
		# even if other Corporations were to have even lower assets on this Market. This might seem redundant because Markets are not supposed to have negative values,
		# but if that changes (unlikely), this'll be ready. It means '0' CANNOT be a superposed state for 'bubble_value', so we don't need 2 fields (for positive and negative bubbles)
		# get all negative bubbles, in alphabetical order of the name of the Market on which they apply
		negative_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, value__lte=0).order_by('market__name'))
		# Turn everything to list, because QuerySets don't have a 'remove' method
		previous_negative_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn - 1, bubble_value=-1).order_by('market__name'))
		# Now get all positive bubbles. We annotate the CorporationMarkets with the field 'maxval', containing the maximal value across all
		positive_bubbles = {}
		max_vals = {}
		for market in Market.objects.all():
			max_vals[market.name] = CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, market=market).exclude(value__lte=0).aggregate(maximum=Max('value'))['maximum']
			if max_vals[market.name] is not None:
				try:
					positive_bubbles[market.name] = CorporationMarket.objects.get(corporation__game=game, turn=game.current_turn, market=market, value=max_vals[market.name])
				except:
					# There were several corporations tied for first
					pass
		previous_positive_bubbles = list(CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn, bubble_value=1))

		modifiers = {}
		for corporation in Corporation.objects.filter(game=game):
			modifiers[corporation] = 0

		for nb in negative_bubbles:
			# DEBUG # print "Negative bubble on %s.%s" % (nb.corporation.base_corporation_slug, nb.market.name)
			# This test differentiates corporations descending to 0, from the ones ascending to 0. The former should get a negative bubble, the latter shouldn't,
			# because the negative bubble are an incentive to get that market back up. If you get it back up to 0, your previous bubble is erased and you don't get a new one.
			# Ascending corporations have a bublle value of -1 because they had a negative bubble last turn, the others do not
			if nb.bubble_value == 0 or nb.value < 0:
				nb.update_bubble(-1)
				nb.save()
				# The following must absolutely be executed in the 'if' and not the 'else', because although the bubbles in the 'else'
				# have been categorized as negative bubbles, they are actually popping this turn because they came back up to 0
				for pnb in previous_negative_bubbles:
					if (pnb.corporation == nb.corporation) and (pnb.market == nb.market):
						# This is not a new bubble
						previous_negative_bubbles.remove(pnb)
						break
				else:
					if after_effects:
						# This bubble did not exist last turn, log its creation
						game.add_event(event_type=game.GAIN_DRY_BUBBLE, data={"market": nb.market.name, "corporation": nb.corporation.base_corporation.name}, corporation=nb.corporation, corporationmarket=nb)
			else:
				# This CorporationMarket had a negative bubble, and came back up: don't shoot the ambulance, actually, help it a bit
				# We do not have to log the bubble popping, it will be logged later, because we haven't removed it from previous_negative_bubbles
				nb.update_bubble(0)
				nb.save()

			# We have to propagate the modification to the corporation's assets_modifier
			modifiers[nb.corporation] += nb.bubble_value

		for pb in positive_bubbles.values():
			# DEBUG
			# print "Positive bubble: %s.%s -> %i (%i)" % (pb.corporation.base_corporation_slug, pb.market.name, pb.value, max_vals[pb.market.name])
			pb.update_bubble(1)
			pb.save()

			modifiers[pb.corporation] += pb.bubble_value

			for ppb in previous_positive_bubbles:
				if (ppb.corporation == pb.corporation) and (ppb.market == pb.market):
					# This is not a new bubble
					previous_positive_bubbles.remove(ppb)
					break
			else:
				if after_effects:
					# This bubble did not exist last turn, log its creation
					game.add_event(event_type=game.GAIN_DOMINATION_BUBBLE, data={"market": pb.market.name, "corporation": pb.corporation.base_corporation.name}, corporation=pb.corporation, corporationmarket=pb)

		# We still have to handle the deletion of the bubbles that burst: We have to log them,
		# But me must mainly decrement value by bubble_value and then also erase the bubble_value
		for pnb in previous_negative_bubbles:
			modifiers[pnb.corporation] -= pnb.bubble_value
			pnb.update_bubble(0)
			pnb.save()
			if after_effects:
				game.add_event(event_type=game.LOSE_DRY_BUBBLE, data={"market": pnb.market.name, "corporation": pnb.corporation.base_corporation.name}, corporation=pnb.corporation, corporationmarket=pnb)

		for ppb in previous_positive_bubbles:
			modifiers[ppb.corporation] -= ppb.bubble_value
			ppb.update_bubble(0)
			ppb.save()
			if after_effects:
				game.add_event(event_type=game.LOSE_DOMINATION_BUBBLE, data={"market": ppb.market.name, "corporation": ppb.corporation.base_corporation.name}, corporation=ppb.corporation, corporationmarket=ppb)

		# DEBUG
		# print "Modifers: "
		# print modifiers
		for corporation in modifiers.keys():
			corporation.update_modifier(modifiers[corporation])
			corporation.save()
		# DEBUG
		# corp_mark = CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn)
		# for cm in corp_mark:
			# print " 2 CorporationMarket: %s.%s -> %i (%i)" % (cm.corporation.base_corporation_slug, cm.market.name, cm.value, cm.bubble_value)


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

		# DEBUG
		# print "----------------------- After effects -------------------------"
		super(UpdateBubblesAfterEffectsTask, self).run(game, after_effects=True)
		return


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
