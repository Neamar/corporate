# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
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

		# Probably a test, but may happen in some situations
		if len(corpos) == 0:
			return

		content=u'La main du marché favorise le marché %s de la corpo %s.' % (corpos[0].historic_market, corpos[0].base_corporation.name)
		corpos[0].update_assets(1)
		game.add_newsfeed(category=Newsfeed.ECONOMY, content=content, status=Newsfeed.PRIVATE, market=corpos[0].historic_market, corpo=corpos[0])

		if len(corpos) >= 2:
			content=u'La main du marché défavorise le marché %s de la corpo %s.' % (corpos[1].historic_market, corpos[1].base_corporation.name)
			corpos[1].update_assets(-1)
			game.add_newsfeed(category=Newsfeed.ECONOMY,content=content , status=Newsfeed.PRIVATE, market=corpos[1].historic_market, corpo=corpos[0])

tasks = (InvisibleHandTask,)
