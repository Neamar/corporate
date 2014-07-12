from engine.exceptions import OrderNotAvailable
from engine.testcases import EngineTestCase
from engine_modules.speculation.models import CorporationSpeculationOrder


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

	def test_corporation_rank_limited(self):
		"""
		Can't speculate on non existing rank
		"""
		o = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.last_corporation,
			rank=self.g.corporation_set.count() + 1,
			investment=5
		)

		self.assertRaises(OrderNotAvailable, o.clean)
