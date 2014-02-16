from engine.testcases import EngineTestCase
from engine_modules.speculation.models import CorporationSpeculationOrder, DerivativeSpeculationOrder, Derivative


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

	def test_derivative_speculation(self):
		"""
		Task should be called
		"""
		self.g.resolve_current_turn()

		self.c.assets = 5
		self.c.save()

		dso = DerivativeSpeculationOrder(
			player=self.p,
			speculation=DerivativeSpeculationOrder.UP,
			investment=5,
			derivative=self.d
		)
		dso.save()

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.p).money, self.initial_money - dso.get_cost())
