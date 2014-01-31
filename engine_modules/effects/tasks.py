from engine.tasks import ResolutionTask

class FirstLastEffectsTask(ResolutionTask):
	"""
	Every time, the first and last corporations have an effect
	"""

	RESOLUTION_ORDER = 600

	def run(self, game):

		ladder = game.get_ordered_corporations()
		first_corporation = corps[0]
		last_corporation = corps[-1]

		first_corporation.on_first_effect()
		last_corporation.on_last_effect()

tasks = (FirstLastEffectsTask, )
