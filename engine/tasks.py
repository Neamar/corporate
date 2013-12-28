class ResolutionTask:
	"""
	A task to call during resolution
	"""

	resolution_order = 0
	name = ""


	def run(self, game):
		raise NotImplementedError("Abstract call.")


class OrderResolutionTask
	"""
	A task to resolve some orders
