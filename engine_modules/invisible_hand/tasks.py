from engine.tasks import ResolutionTask

class InvisibleHandTask(ResolutionTask):
	"""
	Give +1 and -1 asset to two corporation
	"""
	RESOLUTION_ORDER = 400

	def run(self, game):
		# Invisible hand can be disabled, for instance to ease testing
		if hasattr(game, 'disable_invisible_hand'):
			return

		corpos = game.corporation_set.all().order_by('?')[0:2]

		# Probably a test, but may happen in some situations
		if len(corpos) == 0:
			return

		corpos[0].assets += 1

		if len(corpos) >= 2:
			corpos[1].assets -= 1
		[corpo.save() for corpo in corpos]

tasks = (InvisibleHandTask,)
