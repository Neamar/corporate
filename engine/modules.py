from django.conf import settings
import importlib

"""
List of tasks to call for each game resolution
"""
__tasks_list = []

"""
List of available orders
"""
__orders_list = []

"""
List of function to call to setup a new game
"""
__setups_list = []


def try_import(file, name, default=None):
	"""
	Try to import some name from some file,
	Returns default on failure
	"""

	try:
		app = importlib.import_module(file)
		return getattr(app, name)
	except ImportError:
		return default
	except AttributeError:
		return default

for app in settings.INSTALLED_APPS:
	# Only scan engine_modules app
	if 'engine_modules.' not in app:
		continue

	__setups_list += try_import("%s.setup" % app, '__setups__', [])
	__orders_list += try_import("%s.orders" % app, '__orders__', [])
	__tasks_list += try_import("%s.tasks" % app, '__tasks__', [])
