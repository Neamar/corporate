from engine.exceptions import OrderNotAvailable
from engine.testcases import EngineTestCase
from engine_modules.share.models import Share, BuyShareOrder
from engine_modules.corporation.models import Corporation, BaseCorporation


class OrdersTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		bc = BaseCorporation(name="bc1")
		bc.save()

		super(OrdersTest, self).setUp()

		self.c = Corporation.objects.get(base_corporation=bc)
		self.o = BuyShareOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.save()

	def test_order_cost_money(self):
		"""
		Order should cost money
		"""
		self.o.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money - BuyShareOrder.BASE_COST * self.c.assets)

	def test_order_add_share(self):
		"""
		A share should be created
		"""
		self.o.resolve()

		s = Share.objects.get(pk=1)
		self.assertEqual(s.player, self.p)
		self.assertEqual(s.corporation, self.o.corporation)
		self.assertEqual(s.turn, self.p.game.current_turn)

	def test_order_limited_by_influence(self):
		"""
		You can't buy more share than your influence
		"""
		o2 =  BuyShareOrder(
			player=self.p,
			corporation=self.c
		)

		self.assertRaises(OrderNotAvailable, o2.clean)

		self.p.influence.level = 2
		self.p.influence.save()
		# assertNoRaises
		o2.clean()
