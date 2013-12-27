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

	def test_game_turns(self):
		"""
		Check is current_turn can't be greater than total_turn
		"""
		self.g.current_turn = 11
		self.assertRaises(IntegrityError, self.g.save)

	def test_message_author_game_equals_player_game(self):
		"""
		Check if author's game = player's game
		"""

		p2 = Player(game=self.g)
		p2.save()

		g2 = Game(total_turn=20)
		g2.save()

		p3 = Player(game=g2)
		p3.save()

		m = Message(title="titre", author=self.p)
		m.save()
		m.recipient_set.add(p2)
		m.save()

		m2 = Message(title="titre1", author= self.p)
		m2.save()
		

		self.assertRaises(IntegrityError, lambda: m2.recipient_set.add(p3))
