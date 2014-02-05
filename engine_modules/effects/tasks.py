from engine.tasks import ResolutionTask

class FirstLastEffectsTask(ResolutionTask):
	"""
	App first and last corporations effects
	"""

	RESOLUTION_ORDER = 600

	def run(self, game):

		ladder = game.get_ordered_corporations()

		# Retrieve first and last before applying any effect
		first_corporation = ladder[0]
		last_corporation = ladder[-1]

		first_corporation.on_first_effect()
		last_corporation.on_last_effect()

tasks = (FirstLastEffectsTask, )
