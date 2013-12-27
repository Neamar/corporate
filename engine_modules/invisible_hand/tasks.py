from engine.tasks import ResolutionTask

class InvisibleHandTask(ResolutionTask):
	"""
	Give +1 and -1 asset to two corporation
	"""
	priority = 40

	def run(self, game):
		if game.corporation_set.count() > 1:
			corpo_up = game.corporation_set.all().order_by['?'][0]
			corpo_down = game.corporation_set.all()
			corpo_down = corpo_down.exclude(pk=corpo_up.pk).order_by['?'][0]

			corpo_up.assets += 1
			corpo_up.save()

			corpo_down.assets -= 1
			corpo_down.save()
		else :
			corpo_up = game.corporation_set.all()[0]
			corpo_up.assets += 1
			corpo_up.save()

tasks = (InvisibleHandTask,)		

