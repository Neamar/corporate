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
	Try to import `name` from some file,
	Returns `default` on failure
	"""

	try:
		app = importlib.import_module(package)
		return getattr(app, name)
	except ImportError:
		if 'No module named' in str(sys.exc_value):
			return default
		else:
			# For invalid imports, we reraise
			raise
	except AttributeError:
		return default

for app in settings.INSTALLED_APPS:
	# Only scan engine_modules app
	if not app.startswith('engine_modules.') and not (app == 'logs'):
		continue

	orders_list += try_import("%s.models" % app, 'orders', [])
	tasks_list += try_import("%s.tasks" % app, 'tasks', [])

	# Autoload signals as a convenience
	# (will try to import 'none' function, fail but register signals.)
	# #dirty
	try_import("%s.signals" % app, 'none')

# Sort tasks in place, by resolution_order
tasks_list.sort(key=lambda t: t.RESOLUTION_ORDER)
