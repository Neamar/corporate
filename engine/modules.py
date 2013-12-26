

custom_urls = {}

class ResolutionTask:
	"""
	A task to call during resolution
	"""

	priority = 0
	name = ""
	task = lambda game: game


def registerModule(taskBuilder, orders, views, setup):
	"""
	Register a new module for use in the game.
	taskBuilder is a function to retrieve a list of tasks items for resolution
	orders is a list of new orders to add
	views is a dict whose keys are regexp and values associated functions. If a conflict occurs between multiple apps, the last entry prevails.
	setup is a function to call on game initialisation
	"""
