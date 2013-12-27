from engine.testcases import EngineTestCase
from engine_modules.influence.orders import BuyInfluenceOrder


class OrdersTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		super(OrdersTest, self).setUp()
		self.o = BuyInfluenceOrder(
			player=self.p
		)
		self.o.save()

	def test_order_cost_money(self):
		"""
		The new player should have influence of 1
		"""
		self.o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money - BuyInfluenceOrder.BASE_COST * 2)

	def test_order_increment_influence(self):
		"""
		The new player should have influence of 1
		"""
		self.o.resolve()

		self.assertEqual(self.reload(self.p).influence.level, 2)
