# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase


class TasksTest(EngineTestCase):
	def test_assets_saved_on_resolution(self):
		"""
		The game should save the corporation assets on resolution
		"""

		self.g.resolve_current_turn()
		self.assertEqual(self.c.assethistory_set.get(turn=1).assets, self.reload(self.c).assets)

	def test_get_ladder(self):
		"""
		Test rank of turn if no ex-aequo
		"""

		self.c3.assets = 13
		self.c3.save()
		self.c2.assets = 12
		self.c2.save()
		self.c.assets = 11
		self.c.save()
		self.g.resolve_current_turn()

		self.assertEqual(self.g.get_ladder(), [self.c3, self.c2, self.c])

	def test_ex_aequo(self):
		"""
		Test rank of turn if ex-aequo
		"""

		self.c3.assets = 13
		self.c3.save()
		self.c2.assets = 12
		self.c2.save()
		self.c.assets = 11
		self.c.save()
		self.g.resolve_current_turn()

		self.c3.assets = 11
		self.c3.save()
		self.c2.assets = 13
		self.c2.save()
		self.c.assets = 11
		self.c.save()

		self.assertEqual(self.g.get_ladder(), [self.c2, self.c3, self.c])

	def test_stability(self):
		"""
		Test stability of ordering corporation with equals assets from the start
		"""
		basic_setup = self.g.get_ladder()
		self.g.resolve_current_turn()
		turn1 = self.g.get_ladder()

		self.assertEqual(basic_setup, turn1)

	def test_multi_turn(self):
		"""
		Test on more than one turn
		"""
		self.c3.assets = 13
		self.c3.save()
		self.c2.assets = 12
		self.c2.save()
		self.c.assets = 11
		self.c.save()
		self.g.resolve_current_turn()

		self.c3.assets = 11
		self.c3.save()
		self.c2.assets = 11
		self.c2.save()
		self.c.assets = 11
		self.c.save()
		self.g.resolve_current_turn()

		self.c3.assets = 11
		self.c3.save()
		self.c2.assets = 13
		self.c2.save()
		self.c.assets = 11
		self.c.save()

		self.assertEqual(self.g.get_ladder(), [self.c2, self.c3, self.c])
