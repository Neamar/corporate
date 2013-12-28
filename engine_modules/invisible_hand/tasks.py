from engine.tasks import ResolutionTask

class InvisibleHandTask(ResolutionTask):
	"""
	Give +1 and -1 asset to two corporation
	"""
	resolution_order = 400

	def run(self, game):
		corpos = game.corporation_set.all().order_by('?')[0:2]
		if len(corpos) == 0:
			return
		corpos[0].assets += 1
		if len(corpos) >= 2:
			corpos[1].assets -= 1
		[corpo.save() for corpo in corpos]



tasks = (InvisibleHandTask,)		

