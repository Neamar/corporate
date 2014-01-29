from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation
from engine_modules.speculation.models import SpeculationOrder


class OrdersTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="Last", description="looser", initials_assets=1)
		self.bc.save()
		self.bc2 = BaseCorporation(name="Medium", description="useless", initials_assets=10)
		self.bc2.save()
		self.bc3 = BaseCorporation(name="First", description="Winner", initials_assets=100)
		self.bc3.save()

		super(OrdersTest, self).setUp()

		self.last_corporation = self.g.corporation_set.get(base_corporation=self.bc)
		self.medium_corporation = self.g.corporation_set.get(base_corporation=self.bc2)
		self.first_corporation = self.g.corporation_set.get(base_corporation=self.bc3)


	def test_order_cost_money(self):
		"""
		Order should cost money
		"""
		o = SpeculationOrder(
			player=self.p,
			corporation=self.last_corporation,
			rank=1,
			investment=5
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money - 50)

	def test_order_big_success_give_money(self):
		o = SpeculationOrder(
			player=self.p,
			corporation=self.medium_corporation,
			rank=2,
			investment=5
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money + 200)

	def test_order_little_success_first_give_money(self):
		o = SpeculationOrder(
			player=self.p,
			corporation=self.first_corporation,
			rank=1,
			investment=5
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money + 100)

	def test_order_little_success_last_give_money(self):
		o = SpeculationOrder(
			player=self.p,
			corporation=self.last_corporation,
			rank=3,
			investment=5
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money + 100)

