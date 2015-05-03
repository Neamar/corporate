# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from messaging.models import Newsfeed


class CrashCorporationTask(ResolutionTask):
	"""
	Let's crash corporations that didn't make it through the turn
	"""
	RESOLUTION_ORDER = 1000

	def run(self, game):
		# corporations_to_crash = game.corporation_set.filter(assets__lte=0)
		# This does not work because my pinky tells me it should be assets, not market_assets
		# but assets is a property, so we're kinda fucked. I don't want to deal with this now, so I'll leave it for later
		# TODO: Find a fix
		corporations_to_crash = []
		corporations = game.corporation_set.all()
		for corporation in corporations:
			if corporation.assets <= 0:
				corporations_to_crash.append(corporation)

		if not corporations_to_crash:
			return

		ladder = game.get_ladder()
		for corporation in corporations_to_crash:
			corporation.on_crash_effect(ladder)
			corporation.delete()
			game.add_newsfeed(category=Newsfeed.ECONOMY, content=u"La corporation %s a crashé." % corporation.base_corporation.name)

tasks = (CrashCorporationTask,)
