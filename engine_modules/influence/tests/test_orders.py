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
		self.assertEqual(self.p.influence.level, 1)
