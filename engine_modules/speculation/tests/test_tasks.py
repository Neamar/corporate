from engine.testcases import EngineTestCase
from engine_modules.speculation.models import CorporationSpeculationOrder
from engine_modules.derivative.models import Derivative


class TasksTest(EngineTestCase):
	def setUp(self):

		super(TasksTest, self).setUp()

		self.d = Derivative(name="first and last", game=self.g)
		self.d.save()
		self.d.corporations.add(self.c, self.c2)

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
