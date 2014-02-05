from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation
from engine_modules.speculation.models import CorporationSpeculationOrder, DerivativeSpeculationOrder, Derivative


class OrdersTest(EngineTestCase):
	def setUp(self):

		super(OrdersTest, self).setUp()

		self.g.corporation_set.all().delete()

		self.first_corporation = Corporation(base_corporation_slug='ares', assets=100)
		self.g.corporation_set.add(self.first_corporation)
		self.medium_corporation = Corporation(base_corporation_slug='renraku', assets=10)
		self.g.corporation_set.add(self.medium_corporation)
		self.last_corporation = Corporation(base_corporation_slug='shiawase', assets=1)
		self.g.corporation_set.add(self.last_corporation)

		self.d = Derivative(name="first and last")
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

	def test_derivative_success_give_money(self):
		"""
		Success when speculate on derivative should give money
		"""
		self.g.resolve_current_turn()

		self.first_corporation.assets += 50
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

