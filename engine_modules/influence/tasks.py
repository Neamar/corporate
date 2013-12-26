from engine.tasks import ResolutionTask


class BuyInfluenceTask(ResolutionTask):
	"""
	Buy new Influence level
	"""
	priority = 90

	def run(self, game):
		"""
		Retrieve all BuyInfluenceOrder
		"""
		print "Wooog."

tasks = (BuyInfluenceTask,)
