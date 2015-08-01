# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask


class CrashCorporationTask(ResolutionTask):
	"""
	Let's crash corporations that didn't make it through the turn
	"""
	RESOLUTION_ORDER = 1000

	def run(self, game):
		corporations_to_crash = game.corporation_set.filter(assets__lte=0)
		if not corporations_to_crash:
			return

		ladder = game.get_ladder()
		for corporation in corporations_to_crash:
			corporation.on_crash_effect(ladder)
			corporation.delete()

tasks = (CrashCorporationTask,)
