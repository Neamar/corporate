from engine.tasks import ResolutionTask


class InvisibleHandTask(ResolutionTask):
	"""
	Give +1 and -1 asset for two random corporations
	"""
	RESOLUTION_ORDER = 400

	def run(self, game):
		# Invisible hand can be disabled, for instance to ease testing, by setting the "disable_side_effects" flag.
		if hasattr(game, 'disable_side_effects') and not hasattr(game, 'force_invisible_hand'):
			return

		corpos = game.corporation_set.all().order_by('?')[0:2]

		# Probably a test, but may happen in some situations
		if len(corpos) == 0:
			return

		corpos[0].update_assets(1)

		if len(corpos) >= 2:
			corpos[1].update_assets(-1)

tasks = (InvisibleHandTask,)
