from engine.testcases import EngineTestCase
from engine_modules.speculation.models import CorporationSpeculationOrder, DerivativeSpeculationOrder, Derivative


class OrdersTest(EngineTestCase):
	def setUp(self):

		super(OrdersTest, self).setUp()

		self.c.assets = 100
		self.c.save()
		self.first_corporation = self.c

		self.c2.assets = 10
		self.c2.save()
		self.medium_corporation = self.c2

		self.c3.assets = 1
		self.c3.save()
		self.last_corporation = self.c3

		self.d = Derivative(name="first and last", game=self.g)
		self.d.save()
		self.d.corporations.add(self.first_corporation, self.last_corporation)

	def test_corporation_speculation_order_cost_money(self):
		"""
		Order should cost money
		"""
		o = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.last_corporation,
			rank=1,
			investment=5
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money - o.get_cost())

	def test_corporation_speculation_big_success_give_money(self):
		"""
		Success when speculate on a non first/last corpo should give lots of money
		"""
		o = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.medium_corporation,
			rank=2,
			investment=5
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money + o.get_cost() * 4)

	def test_corporation_speculation_little_success_first_give_money(self):
		"""
		Success when speculate on a first corpo should give money
		"""
		o = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.first_corporation,
			rank=1,
			investment=5
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money + o.get_cost() * 2)

	def test_corporation_speculation_little_success_last_give_money(self):
		"""
		Success when speculate on a last corpo should give money
		"""
		o = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.last_corporation,
			rank=3,
			investment=5
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money + o.get_cost() * 2)

	def test_derivative_failure_remove_money(self):
		"""
		Derivative speculation failure  cost money
		"""
		self.g.resolve_current_turn()

		self.first_corporation.assets -= 5
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

	def test_derivative_success_give_money(self):
		"""
		Success when speculate on derivative should give money
		"""
		self.g.resolve_current_turn()

		self.first_corporation.assets += 5
		self.first_corporation.save()

		dso = DerivativeSpeculationOrder(
			player=self.p,
			speculation=DerivativeSpeculationOrder.UP,
			investment=5,
			derivative=self.d
		)
		dso.save()

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.p).money, self.initial_money + dso.get_cost() * 2)
