class ResolutionTask:
	"""
	An abstract task to call during resolution
	"""
	RESOLUTION_ORDER = 0

	def run(self, game):
		raise NotImplementedError("Abstract call.")


class OrderResolutionTask(ResolutionTask):
	"""
	A task to resolve all orders of some kind,
	where sorting is irrelevant
	"""
	ORDER_TYPE = None

	def run(self, game):
		"""
		Retrieve all ORDER_TYPE items and resolve them
		"""
		orders = self.ORDER_TYPE.objects.filter(player__game=game, turn=game.current_turn)

		for order in orders:
			order.resolve()
