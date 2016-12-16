from engine.exceptions import OrderNotAvailable

from engine.testcases import EngineTestCase
from engine_modules.influence.models import BuyInfluenceOrder


class OrdersTest(EngineTestCase):
	def setUp(self):
		super(OrdersTest, self).setUp()
		self.o = BuyInfluenceOrder(
			player=self.p
		)
		self.o.clean()
		self.o.save()

	def test_order_cost_money(self):
		"""
		Money should be reduced
		"""
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).money, self.initial_money - BuyInfluenceOrder.BASE_COST)

	def test_order_increment_influence(self):
		"""
		Order should increment influence
		"""
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).influence.level, 2)

	def test_cant_create_order_twice(self):
		"""
		Order can't be created twice
		"""
		o2 = BuyInfluenceOrder(
			player=self.p
		)

		self.assertRaises(OrderNotAvailable, o2.clean)
