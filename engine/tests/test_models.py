# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine.models import Player, Order
from website.models import User


class ModelsTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def test_game_turns(self):
		"""
		Check if current_turn can't be greater than total_turn
		"""

		self.g.current_turn = 11
		self.assertRaises(IntegrityError, self.g.save)

	def test_game_no_two_players_from_same_user_in_game(self):
		"""
		Check if a user can't have 2 players in the same game
		"""

		u = User(username="haha", email="azre@fer.fr")
		u.save()

		self.p.user = u
		self.p.save()

		p2 = Player(user=u, game=self.g)
		self.assertRaises(IntegrityError, p2.save)

	def test_game_resolve_current_turn_updates_current_turn_value(self):
		"""
		Check if the current turn is incremented
		"""

		self.g.current_turn = 1
		self.g.save()

		self.g.resolve_current_turn()

		self.assertEqual(self.g.current_turn, 2)

	def test_order_clean_is_abstract(self):
		"""
		Check a raw Order can't be created
		"""

		o = Order(player=self.p)
		self.assertRaises(ValidationError, o.clean)

	def test_order_resolve_is_abstract(self):
		"""
		Check a raw Order can't be created
		"""

		o = Order(player=self.p)
		self.assertRaises(NotImplementedError, o.resolve)

	def test_order_description_is_abstract(self):
		"""
		Check a raw Order can't be created
		"""

		o = Order(player=self.p)
		self.assertRaises(NotImplementedError, o.description)

	def test_order_save_autoset_turn(self):
		"""
		Check is save() autoset the right turn
		"""

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
		Can't create an order pointing to another turn than the current one
		"""

		o = Order(player=self.p, turn=2)

		self.assertRaises(IntegrityError, o.save)

	def test_order_modification_during_another_turn(self):
		"""
		Can't modify the turn from an existing order
		"""

		o = Order(player=self.p)
		o.save()

		o.turn = 2

		self.assertRaises(IntegrityError, o.save)

	def test_order_cant_create_without_money(self):
		"""
		Order can't be created without enough money
		"""
		class SomeOrder(Order):
			class Meta:
				proxy = True

			def get_cost(self):
				return 1

		self.p.money = 0
		self.p.save()

		o = SomeOrder(
			player=self.p
		)

		self.assertRaises(ValidationError, o.clean)

	def test_order_cant_create_without_money_for_other_order(self):
		"""
		Order can't be created without enough money to cover for existing orders
		"""
		class SomeExpensiveOrder(Order):
			class Meta:
				proxy = True

			def get_cost(self):
				return self.player.money

		o = SomeExpensiveOrder(
			player=self.p
		)
		# Should not raise any exception
		o.clean()
		o.save()

		o2 = SomeExpensiveOrder(
			player=self.p
		)
		# But you can't stack them
		self.assertRaises(ValidationError, o2.clean)

	def test_player_money_cant_be_negative(self):
		"""
		Check if money can't be test_money_cant_be_negative
		"""

		self.p.money = 100
		self.p.save()

		self.p.money -= 120

		self.assertRaises(IntegrityError, self.p.save)

	def test_player_get_current_orders_returns_only_current_orders(self):
		"""
		Check if get_current_orders return only current orders
		"""

		o = Order(player=self.p)
		o.save()

		self.g.current_turn = 2
		self.g.save()
		o2 = Order(player=self.p)
		o2.save()

		self.g.current_turn = 3
		self.g.save()
		o3 = Order(player=self.p)
		o3.save()

		self.g.current_turn = 2
		self.g.save()

		self.assertEqual([o2], list(self.p.get_current_orders()))
