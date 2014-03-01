from engine.tasks import ResolutionTask
from messaging.models import Newsfeed


class FirstLastEffectsTask(ResolutionTask):
	"""
	Apply first and last corporations effects
	"""

	RESOLUTION_ORDER = 600

	def run(self, game):
		# Effects can be disabled, for instance to ease testing, by setting the "disable_side_effects" flag.
		if hasattr(game, 'disable_side_effects') and not hasattr(game, "force_first_last_effects"):
			return

		ladder = game.get_ladder()

		# Retrieve first and last before applying any effect
		first_corporation = ladder[0]
		last_corporation = ladder[-1]

		first_corporation.on_first_effect(ladder)
		last_corporation.on_last_effect(ladder)

		game.add_newsfeed(category=Newsfeed.ECONOMY, content="Effet premier : %s, effet dernier : %s" % (first_corporation.base_corporation.name, last_corporation.base_corporation.name))

tasks = (FirstLastEffectsTask, )
