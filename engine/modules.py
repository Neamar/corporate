from django.conf import settings
import importlib

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


def try_import(package, name, default=None):
	"""
	Try to import some name from some file,
	Returns default on failure
	"""

	try:
		app = importlib.import_module(package)
		return getattr(app, name)
	except ImportError:
		return default
	except AttributeError:
		return default

for app in settings.INSTALLED_APPS:
	# Only scan engine_modules app
	if 'engine_modules.' not in app:
		continue

	# setups_list += try_import("%s.setup" % app, 'setups', [])
	orders_list += try_import("%s.orders" % app, 'orders', [])
	tasks_list += try_import("%s.tasks" % app, 'tasks', [])

# Sort tasks in place, by priority
tasks_list.sort(key=lambda t: t.priority)
