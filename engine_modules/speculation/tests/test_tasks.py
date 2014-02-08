from engine.testcases import EngineTestCase
from engine_modules.speculation.models import CorporationSpeculationOrder, DerivativeSpeculationOrder, Derivative


class TasksTest(EngineTestCase):
	def setUp(self):

		super(TasksTest, self).setUp()

		self.c.assets = 100
		self.c.save()
		self.first_corporation = self.c

		self.c2.assets = 10
		self.c2.save()
		self.medium_corporation = self.c2

		self.c3.assets = 1
		self.c3.save()
		self.last_corporation = self.c3

		self.d = Derivative(name="first and last")
		self.d.save()
		self.d.corporations.add(self.first_corporation, self.last_corporation)

	def test_corporation_speculation(self):
		"""
		Task should be called
		"""
		cso = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.first_corporation,
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

		self.first_corporation.assets -= 50
		self.first_corporation.save()

		dso = DerivativeSpeculationOrder(
			player=self.p,
			speculation=DerivativeSpeculationOrder.UP,
			investment=5,
			derivative=self.d
		)
		dso.save()
		
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.p).money, self.initial_money - dso.get_cost())
