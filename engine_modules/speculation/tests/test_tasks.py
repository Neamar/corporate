from engine.testcases import EngineTestCase
from engine_modules.speculation.models import CorporationSpeculationOrder


class TasksTest(EngineTestCase):
	def setUp(self):

		super(TasksTest, self).setUp()

	def test_corporation_speculation(self):
		"""
		Task should be called
		"""
		self.c.assets = 50
		self.c.save()

		cso = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.c,
			rank=1,
			investment=5
		)
		cso.save()

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.p).money, self.initial_money + cso.get_cost() * 2)
