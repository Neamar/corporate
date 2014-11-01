import sys

from django.db import transaction
from django.test import TestCase
from django.conf import settings

from engine.models import Game
from engine_modules.corporation.models import BaseCorporation


class ManhattanEffectsTest(TestCase):
	"""
	Retrieve all Manhattan corporations, and check their first and last effects
	"""

	@classmethod
	def setUpClass(self):
		# Override to use Manhattan
		MANHATTAN_BASE_DIR = "%s/data/cities/manhattan" % settings.BASE_DIR
		BaseCorporation.BASE_CORPORATION_DIR = BaseCorporation.BASE_CORPORATION_TEMPLATE % MANHATTAN_BASE_DIR

		BaseCorporation.build_dict()
		self.g = Game()
		self.g.save()

	@classmethod
	def tearDownClass(self):
		BaseCorporation.BASE_CORPORATION_DIR = BaseCorporation.BASE_CORPORATION_TEMPLATE % settings.CITY_BASE_DIR
		BaseCorporation.build_dict()
		self.g.delete()

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

	def test_all_corporations_last_effect(self):
		"""
		Checking for all corporation last_effects
		"""
		ladder = self.g.get_ladder()
		for corporation in self.g.corporation_set.all():
			sid = transaction.savepoint()
			try:
				corporation.on_last_effect(ladder)
			except:
				e = sys.exc_value
				message = "[%s.on_last_effect] %s" % (corporation.base_corporation_slug, str(e))
				raise e.__class__(message)
			transaction.savepoint_rollback(sid)
