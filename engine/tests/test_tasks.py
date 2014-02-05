from engine.testcases import EngineTestCase

from engine.tasks import ResolutionTask


class TaskTest(EngineTestCase):
	def test_task_run_is_abstract(self):
		"""
		Check if current_turn can't be greater than total_turn
		"""

		t = ResolutionTask()
		self.assertRaises(NotImplementedError, lambda: t.run(None))

	def test_task_applied_once(self):
		"""
		Check a task is only applied once, and not every turn
		"""
		from engine_modules.influence.models import BuyInfluenceOrder

		o = BuyInfluenceOrder(
			player=self.p
		)
		o.save()

		start_influence = self.p.influence.level
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).influence.level, start_influence + 1)

		# Check order is only applied on creation turn, not every turn
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).influence.level, start_influence + 1)
