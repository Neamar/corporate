from django.db import IntegrityError

from engine.testcases import EngineTestCase


class DispatchTest(EngineTestCase):
	def test_post_create_signal(self):
		"""
		Check is current_turn can't be greater than total_turn
		"""
		self.g.current_turn = self.g.total_turn + 1
		self.assertRaises(IntegrityError, self.g.save)
