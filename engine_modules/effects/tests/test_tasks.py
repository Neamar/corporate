from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation
from engine_modules.effects.tasks import FirstLastEffectsTask

class TasksTest(EngineTestCase):
	def setUp(self):

		super(TasksTest, self).setUp()

		self.g.corporation_set.all().delete()

		self.first_corporation = Corporation(base_corporation_slug='renraku', assets=20)
		self.g.corporation_set.add(self.first_corporation)
		self.medium_corporation = Corporation(base_corporation_slug='shiawase', assets=1)
		self.g.corporation_set.add(self.medium_corporation)
		self.last_corporation = Corporation(base_corporation_slug='ares', assets=5)
		self.g.corporation_set.add(self.last_corporation)

	def test_first_effect(self):

		self.g.resolve_current_turn()
		#self.assertEqual(self.first_corporation.assets, 31337)
