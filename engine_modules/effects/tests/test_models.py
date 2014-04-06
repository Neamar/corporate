import sys

from django.db import transaction
from django.test import TestCase

from engine.models import Game


class ModelTest(TestCase):
	"""
	Inherit from test case, to retrieve all corporations
	"""
	def setUp(self):
		self.g = Game()
		self.g.save()

	def test_all_corporations_first_effect(self):
		"""
		Checking for all corporation first_effects
		"""
		ladder = self.g.get_ladder()
		for corporation in self.g.corporation_set.all():
			sid = transaction.savepoint()
			try:
				corporation.on_first_effect(ladder)
			except:
				e = sys.exc_value
				message = "[%s.on_first_effect] %s" % (corporation.base_corporation_slug, str(e))
				raise e.__class__(message)
			transaction.savepoint_rollback(sid)
