# -*- coding: utf-8 -*-
from engine.models import Game
from engine.tasks import ResolutionTask
from engine_modules.corporation.models import AssetDelta
from engine_modules.market.models import CorporationMarket


class InvisibleHandTask(ResolutionTask):
	"""
	Give +1 and -1 asset for two random corporations
	"""
	RESOLUTION_ORDER = 400

	def run(self, game):
		# We can force the invisible hand using the force_invisible_hand flag
		if game.disable_side_effects and not hasattr(game, 'force_invisible_hand'):
			return

		corporation_market = CorporationMarket.objects.filter(corporation__game=game, turn=game.current_turn).order_by('?')[0]
		corporation_market.corporation.update_assets(1, category=AssetDelta.INVISIBLE_HAND, corporation_market=corporation_market)
		game.add_event(event_type=Game.MARKET_HAND_UP, data={"market": corporation_market.market.name, "corporation": corporation_market.corporation.base_corporation.name}, delta=1, corporation=corporation_market.corporation, corporation_market=corporation_market)

		# Only get cm above 0
		corporation_market = CorporationMarket.objects.filter(corporation__game=game, value__gt=0, turn=game.current_turn).exclude(pk=corporation_market.pk).order_by('?')[0]
		corporation_market.corporation.update_assets(-1, category=AssetDelta.INVISIBLE_HAND, corporation_market=corporation_market)
		game.add_event(event_type=Game.MARKET_HAND_DOWN, data={"market": corporation_market.market.name, "corporation": corporation_market.corporation.base_corporation.name}, delta=-1, corporation=corporation_market.corporation, corporation_market=corporation_market)

tasks = (InvisibleHandTask,)
