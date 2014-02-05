import importlib
import sys

from django.conf import settings

"""
List of tasks to call for each game resolution
"""
tasks_list = []

"""
List of available orders
"""
orders_list = []


def try_import(package, name, default=None):
	"""
	Try to import some name from some file,
	Returns default on failure
	"""

	try:
		app = importlib.import_module(package)
		return getattr(app, name)
	except ImportError:
		if 'No module named' in str(sys.exc_value):
			return default
		else:
			raise
	except AttributeError:
		return default

for app in settings.INSTALLED_APPS:
	# Only scan engine_modules app
	if 'engine_modules.' not in app:
		continue

	orders_list += try_import("%s.models" % app, 'orders', [])
	tasks_list += try_import("%s.tasks" % app, 'tasks', [])

	# Autoload signals as a convenience
	try_import("%s.signals" % app, 'none')


# Sort tasks in place, by resolution_order
tasks_list.sort(key=lambda t: t.RESOLUTION_ORDER)
