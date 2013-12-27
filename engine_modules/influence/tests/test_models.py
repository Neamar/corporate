from django.test import TestCase
from engine.models import Game, Player, Message, Order
from django.db import IntegrityError


class ModelTest(TestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		self.g = Game(total_turn=10)
		self.g.save()
		self.p = Player(game=self.g)
		self.p.save()

	def test_influence_auto_created(self):
		"""
		The new player should have influence of 1
		"""
		self.assertEqual(self.p.influence.level, 1)
