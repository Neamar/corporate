from django.test import TestCase

from engine.tasks import ResolutionTask
class TaskTest(TestCase):
	def test_task_run_is_abstract(self):
		"""
		Check if current_turn can't be greater than total_turn
		"""

		t = ResolutionTask()
		self.assertRaises(NotImplementedError, lambda: t.run(None))
