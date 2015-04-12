# -*- coding: utf-8 -*-

from engine.tasks import ResolutionTask
from engine_modules.corporation.models import AssetDelta
from messaging.models import Newsfeed


class InvisibleHandTask(ResolutionTask):
	"""
	Give +1 and -1 asset for two random corporations
	"""
	RESOLUTION_ORDER = 400

	def run(self, game):
		# We can force the invisible hand using the force_invisible_hand flag
		if game.disable_side_effects and not hasattr(game, 'force_invisible_hand'):
			return

		corpos = game.corporation_set.all().order_by('?')[0:2]

		# Probably a useless test, but may happen in some situations
		if len(corpos) == 0:
			return

		market = corpos[0].get_random_market()
		corpos[0].update_assets(1, category=AssetDelta.INVISIBLE_HAND, market=market)
		content = u'La main du marché favorise le marché %s de la corpo %s.' % (market.name, corpos[0].base_corporation.name)
		game.add_newsfeed(category=Newsfeed.ECONOMY, content=content, status=Newsfeed.PRIVATE, market=market, corporations=[corpos[0]])

		if len(corpos) >= 2:
			market = corpos[1].get_random_market()
			corpos[1].update_assets(-1, category=AssetDelta.INVISIBLE_HAND, market=market)
			content = u'La main du marché défavorise le marché %s de la corpo %s.' % (market.name, corpos[1].base_corporation.name)
			game.add_newsfeed(category=Newsfeed.ECONOMY, content=content, status=Newsfeed.PRIVATE, market=market, corporations=[corpos[1]])

tasks = (InvisibleHandTask,)
