# -*- coding: utf-8 -*-
from engine.exceptions import OrderNotAvailable
from engine.testcases import EngineTestCase
from engine_modules.share.models import Share, BuyShareOrder
from engine_modules.corporation.models import Corporation
from messaging.models import Note


class OrdersTest(EngineTestCase):
	def setUp(self):

		super(OrdersTest, self).setUp()

		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='renraku', assets=7)
		self.c2 = Corporation(base_corporation_slug='shiawase', assets=8)
		self.g.corporation_set.add(self.c)
		self.g.corporation_set.add(self.c2)

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

		self.p.influence.level = 2
		self.p.influence.save()
		# assertNoRaises
		o2.clean()

	def test_order_message(self):
		"""
		Note differ after first share
		"""
		self.o.resolve()
		n = Note.objects.filter(category="Parts").last()
		self.assertTrue(u'première' in n.content)

		self.o.resolve()
		n = Note.objects.filter(category="Parts").last()
		self.assertTrue(u'2ème' in n.content)

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
		self.p.citizenship.corporation = self.c2
		self.p.citizenship.save()

		init_money = self.p.money

		o2 = BuyShareOrder(
			player=self.p,
			corporation=self.c2
		)
		o2.save()
		o2.resolve()

		self.assertEqual(self.reload(self.p).money, init_money - BuyShareOrder.FIRST_AND_CITIZEN_COST * self.c2.assets)
