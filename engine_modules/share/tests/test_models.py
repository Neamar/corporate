from django.db import IntegrityError

from engine.testcases import EngineTestCase
from engine.models import Game
from engine_modules.share.models import Share


class ModelsTest(EngineTestCase):
	def setUp(self):

		super(ModelsTest, self).setUp()

	def test_share_creation_automatically_set_turn(self):
		"""
		Share should be created at current turn
		"""
		s = Share(
			corporation=self.c,
			player=self.p
		)
		s.save()

		self.assertEqual(s.turn, self.g.current_turn)

	def test_share_cant_be_updated(self):
		"""
		Share should be created at current turn
		"""
		s = Share(
			corporation=self.c,
			player=self.p
		)
		s.save()

		self.g.current_turn += 1
		self.g.save()

		self.assertRaises(IntegrityError, s.save)

	def test_share_integrity(self):
		"""
		Share corporation must be part of the same game as the player
		"""
		g2 = Game()
		g2.save()

		s = Share(
			corporation=g2.corporations['c'],
			player=self.p
		)

		self.assertRaises(IntegrityError, s.save)
