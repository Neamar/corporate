from engine.tasks import ResolutionTask


class FirstLastEffectsTask(ResolutionTask):
	"""
	Apply first and last corporations effects
	"""

	RESOLUTION_ORDER = 600

	def run(self, game):
		# We can force the first and last effects using the force_first_last_effects flag
		if game.disable_side_effects and not hasattr(game, "force_first_last_effects"):
			return

		ladder = game.get_ladder()

		# Retrieve first and last before applying any effect
		first_corporation = ladder[0]
		last_corporation = ladder[-1]

		first_corporation.on_first_effect(ladder)
		ladder = game.get_ladder()
		new_last_corporation = ladder[-1]
		# We apply last effect only if no corporation will crash this turn
		if new_last_corporation.assets > 0:
			last_corporation.on_last_effect(ladder)

tasks = (FirstLastEffectsTask, )
