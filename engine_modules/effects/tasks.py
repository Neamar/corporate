from engine.tasks import ResolutionTask
from messaging.models import Newsfeed


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

		game.add_newsfeed(category=Newsfeed.ECONOMY, content="Effet premier : %s, effet dernier : %s" % (first_corporation.base_corporation.name, last_corporation.base_corporation.name))

tasks = (FirstLastEffectsTask, )
