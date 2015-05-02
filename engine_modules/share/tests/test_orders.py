# -*- coding: utf-8 -*-
from engine.exceptions import OrderNotAvailable
from engine.testcases import EngineTestCase
from engine_modules.share.models import Share, BuyShareOrder
from messaging.models import Note


class OrdersTest(EngineTestCase):
	def setUp(self):

		super(OrdersTest, self).setUp()
		self.c3.delete()

		self.c.assets = 7
		self.c.save()

		self.c2.assets = 8
		self.c2.save()

		self.o = BuyShareOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.save()

	def test_order_cost_money(self):
		"""
		Order should cost money
		"""
		init_money = self.p.money
		self.o.resolve()
		self.assertEqual(self.reload(self.p).money, init_money - BuyShareOrder.BASE_COST * self.c.assets)

	def test_order_add_share(self):
		"""
		A share should be created
		"""
		self.o.resolve()
		s = Share.objects.get()
		self.assertEqual(s.player, self.p)
		self.assertEqual(s.corporation, self.o.corporation)
		self.assertEqual(s.turn, self.p.game.current_turn)

	def test_order_limited_by_influence(self):
		"""
		You can't buy more shares than your influence
		"""
		o2 = BuyShareOrder(
			player=self.p,
			corporation=self.c
		)

		self.assertRaises(OrderNotAvailable, o2.clean)

		influence = self.p.influence
		influence.level = 2
		influence.save()
		# assertNoRaises
		o2.clean()

	def test_order_message(self):
		"""
		Note differ after first share
		"""
		self.o.resolve()
		n = Note.objects.filter(category=Note.GLOBAL).last()
		self.assertIn(u'première', n.content)

		self.o.resolve()
		n = Note.objects.filter(category=Note.GLOBAL).last()
		self.assertIn(u'2<sup>ème</sup>', n.content)

	def test_order_special_cost_for_first_corpo_and_not_citizen(self):
		"""
		Share should cost more money when corporation is first
		"""
		init_money = self.p.money

		o2 = BuyShareOrder(
			player=self.p,
			corporation=self.c2
		)
		o2.save()
		o2.resolve()

		self.assertEqual(self.reload(self.p).money, init_money - BuyShareOrder.FIRST_COST * self.c2.assets)

	def test_order_special_cost_for_first_corpo_and_citizen(self):
		"""
		Order should cost FIRST_AND_CITIZEN_COST rate when corporation is first and we have the citizenship
		"""
		citizenship = self.p.citizenship
		citizenship.corporation = self.c2
		citizenship.save()
		self.g.resolve_current_turn()

		init_money = self.p.money

		o2 = BuyShareOrder(
			player=self.p,
			corporation=self.c2
		)
		o2.save()
		o2.resolve()

		self.assertEqual(self.reload(self.p).money, init_money - BuyShareOrder.FIRST_AND_CITIZEN_COST * self.c2.assets)
