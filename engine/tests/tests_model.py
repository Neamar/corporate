from django.db import IntegrityError

from engine.testcases import EngineTestCase
from engine.models import Game, Player, Message, Order
from website.models import User

class ModelTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
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

	def test_no_two_layer_from_same_user_in_game(self):
		"""
		Check if a user can't have 2 players in the same game
		"""
		u = User(username="haha", email="azre@fer.fr")
		u.save()

		self.p.user = u
		self.p.save()

		p2 = Player(user=u, game=self.g)
		self.assertRaises(IntegrityError, p2.save)

	def test_resolve_current_turn_updates_current_turn_value(self):
		"""
		Check if the current turn is incremented
		"""
		self.g.current_turn=1
		self.g.save()

		self.g.resolve_current_turn()

		self.assertEqual(self.g.current_turn, 2)

	def test_player_get_current_orders_returns_only_current_orders(self):
		"""
		Check if get_current_orders return only current orders
		"""
		self.g.current_turn=1
		self.g.save()
		o = Order(player=self.p)
		o.save()

		self.g.current_turn=2
		self.g.save()
		o2 = Order(player=self.p)
		o2.save()

		self.g.current_turn=3
		self.g.save()
		o3 = Order(player=self.p)
		o3.save()

		self.g.current_turn=2
		self.g.save()

		self.assertEqual([o2], list(self.p.get_current_orders()))

	def test_order_save_autoset_turn(self):
		"""
		Check is save() autoset the right turn
		"""
		self.g.current_turn=1
		self.g.save()

		o = Order(player=self.p)
		o.save()

		self.assertEqual(1, o.turn)

	def test_order_save_autoset_type(self):
		"""
		Check if save() autoset the right type
		"""
		class TestOrder(Order):
			class Meta:
				proxy = True
			
		o = TestOrder(player=self.p)
		o.save()

		self.assertEqual(o.type, "TestOrder")

	def test_order_creation_during_another_turn(self):
		"""
		Check if an order can't be created at another turn
		"""
		self.g.current_turn=1
		self.g.save()

		o = Order(player=self.p, turn=2)

		self.assertRaises(IntegrityError, o.save)


	def test_order_modification_during_another_turn(self):
		"""
		Check if an order can't be modified at another turn
		"""
		self.g.current_turn=1
		self.g.save()

		o = Order(player=self.p, turn=1)
		o.save()

		o.turn = 2

		self.assertRaises(IntegrityError, o.save)

