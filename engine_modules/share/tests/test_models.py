from django.db import IntegrityError

from engine.testcases import EngineTestCase
from engine.models import Game
from engine_modules.corporation.models import BaseCorporation, Corporation
from engine_modules.share.models import Share


class ModelTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless.")
		self.bc.save()

		super(ModelTest, self).setUp()

	def test_share_creation_automatically_set_turn(self):
		"""
		Share should be created at current turn
		"""
		s = Share(
			corporation=self.g.corporation_set.get(base_corporation=self.bc),
			player=self.p
		)
		s.save()

		self.assertEqual(s.turn, self.g.current_turn)

	def test_share_integrity(self):
		"""
		Share corporation must be part of the same game as the player
		"""
		g2 = Game(total_turn=10)
		g2.save()

		s = Share(
			corporation=g2.corporation_set.get(base_corporation=self.bc),
			player=self.p
		)
		
		self.assertRaises(IntegrityError, s.save)
