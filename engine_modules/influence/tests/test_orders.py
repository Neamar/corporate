from django.test import TestCase
from django.db import IntegrityError

from engine.models import Game, Player
from engine_modules.influence.orders import BuyInfluenceOrder


class OrdersTest(TestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		self.g = Game(total_turn=10)
		self.g.save()
		self.p = Player(game=self.g)
		self.p.save()
		self.o = BuyInfluenceOrder(
			player=self.p
		)
		self.o.save()

	def test_order_cost_money(self):
		"""
		The new player should have influence of 1
		"""
		initial_money = 1000000
		self.p.money = initial_money
		self.p.save()
		self.p.influence.level = 1
		self.p.influence.save()

		self.g.resolve_current_turn()

		self.assertEqual(Player.objects.get(pk=self.p.pk).money, initial_money - BuyInfluenceOrder.BASE_COST * 2)
