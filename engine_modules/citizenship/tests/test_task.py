from engine.testcases import EngineTestCase
from engine_modules.citizenship.models import CitizenShipOrder
from engine_modules.corporation.models import Corporation


class TasksTest(EngineTestCase):
	def setUp(self):
		super(TasksTest, self).setUp()
		
		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='renraku', assets=10)
		self.g.corporation_set.add(self.c)

		self.o = CitizenShipOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.save()

	def test_tasks_applied(self):
		"""
		The new player should have a citizenship in the new corporation
		"""
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).citizenship.corporation, self.c)
