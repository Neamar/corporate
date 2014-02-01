from django.conf import settings

from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation, BaseCorporation
from engine_modules.effects.tasks import FirstLastEffectsTask

class TasksTest(EngineTestCase):
	def setUp(self):

		super(TasksTest, self).setUp()

		self.g.corporation_set.all().delete()

		# We modify the base corporations
		TEST_BASE_CORPORATIONS_DIR = "%s/engine_modules/effects/tests/base_corporations_test" %(settings.BASE_DIR)
		BaseCorporation.base_corporations = BaseCorporation.build_corpo_dict(TEST_BASE_CORPORATIONS_DIR)

		self.first_corporation = Corporation(base_corporation_slug='testrenraku', assets=20)
		self.g.corporation_set.add(self.first_corporation)
		self.medium_corporation = Corporation(base_corporation_slug='testshiawase', assets=10)
		self.g.corporation_set.add(self.medium_corporation)
		self.last_corporation = Corporation(base_corporation_slug='testares', assets=5)
		self.g.corporation_set.add(self.last_corporation)

	def tearDown(self):
		# Because the test modifies BaseCorporation, we have to cleanup (the other tests do not import engine_modules.corporation.models)
		# So the class is not initialized. To protect performance, we cleanup here instead of initializing everywhere
		BaseCorporation.generate_dict()
		super(TasksTest, self).tearDown()

	def test_first_effect(self):
		"""
		Test that the first corporation's on_first effect gets applied
		"""

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.first_corporation).assets, 31337)
