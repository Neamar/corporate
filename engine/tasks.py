class ResolutionTask:
	"""
	A task to call during resolution
	"""

	priority = 0
	name = ""


	def run(self, game):
		raise Exception("Abstract call.")
