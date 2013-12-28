from engine.testcases import EngineTestCase
from engine_modules.citizenship.models import CitizenShipOrder
from engine_modules.corporation.models import BaseCorporation, Corporation


class TasksTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless.")
		self.bc.save()
		super(TasksTest, self).setUp()
		self.c = Corporation.objects.get(base_corporation=self.bc)

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
