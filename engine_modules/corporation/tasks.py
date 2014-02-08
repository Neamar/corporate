from engine.tasks import ResolutionTask


class CrashCorporationTask(ResolutionTask):
	"""
	Let's crash corporations that didn't made it throuh the turn
	"""
	resolution_order = 1000

	def run(self, game):
		corporations_to_crash = game.corporation_set.filter(assets__lte=0)
		for corporation in corporations_to_crash:
			corporation.delete()

tasks = (CrashCorporationTask,)
