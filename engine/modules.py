

"""
List of tasks to call for each game resolution
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


	def run(self, game):
		raise Exception("Abstract call.")


def register_module(tasks=[], orders=[], views={}, setup=None):
	"""
	Register a new module for use in the game.
	tasks_list is an array of ResolutionTask subclasses
	views is a dict whose keys are regexp and values associated functions. If a conflict occurs between multiple apps, the last entry prevails.
	setup is a function to call on game initialisation
	"""
	global tasks_list, orders_list, setups_list, views_list
	
	if tasks:
		tasks_list.append(tasks)

	if setup:
		setups_list.append(setup)

	orders_list += orders
	views_list.update(views)


