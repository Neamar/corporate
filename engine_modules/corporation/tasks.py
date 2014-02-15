# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from messaging.models import Newsfeed


class CrashCorporationTask(ResolutionTask):
	"""
	Let's crash corporations that didn't made it throuh the turn
	"""
	RESOLUTION_ORDER = 1000

	def run(self, game):
		corporations_to_crash = game.corporation_set.filter(assets__lte=0)
		for corporation in corporations_to_crash:
			corporation.delete()
			game.add_newsfeed(category=Newsfeed.ECONOMY, content=u"La corporation %s a crashée" % corporation.base_corporation.name)

tasks = (CrashCorporationTask,)
