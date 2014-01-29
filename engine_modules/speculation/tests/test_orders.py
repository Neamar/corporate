from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation
from engine_modules.speculation.models import SpeculationOrder


class OrdersTest(EngineTestCase):
	def setUp(self):

		super(OrdersTest, self).setUp()

		self.g.corporation_set.all().delete()

		self.first_corporation = Corporation(base_corporation_slug='Last', assets=100)
		self.g.corporation_set.add(self.first_corporation)
		self.medium_corporation = Corporation(base_corporation_slug='Medium', assets=10)
		self.g.corporation_set.add(self.medium_corporation)
		self.last_corporation = Corporation(base_corporation_slug='First', assets=1)
		self.g.corporation_set.add(self.last_corporation)

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

