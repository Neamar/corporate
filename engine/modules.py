

"""
List of task builder to call before each game resolution
"""
tasks_list = []

"""
List of available orders
"""
orders_list = []

"""
List of function to call to setup a new game
"""
setups_list = []

"""
List of custom urls
"""
views_list = {}

class ResolutionTask:
	"""
	A task to call during resolution
	"""

	priority = 0
	name = ""
	task = lambda game: game


def registerModule(task_builder=None, orders=[], views={}, setup=None):
	"""
	Register a new module for use in the game.
	taskBuilder is a function to retrieve a list of tasks items for resolution
	orders is a list of new orders to add
	views is a dict whose keys are regexp and values associated functions. If a conflict occurs between multiple apps, the last entry prevails.
	setup is a function to call on game initialisation
	"""
	global tasks_list, orders_list, setups_list, views_list
	
	if task_builder:
		tasks_list.append(task_builder)

	if setup:
		setups_list.append(setup)

	orders_list += orders
	views_list.update(views)


