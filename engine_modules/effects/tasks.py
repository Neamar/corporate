from engine.tasks import ResolutionTask

class FirstLastEffectsTask(ResolutionTask):
	"""
	Every time, the first and last corporations have an effect
	"""

	RESOLUTION_ORDER = 600

	def run(self, game):

		corps = game.get_ordered_corporations()
		first_corp = corps[0]
		last_corp = corps[-1]

		first_corp.on_first_effect()
		last_corp.on_last_effect()

tasks = (FirstLastEffectsTask, )
