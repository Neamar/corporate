from engine.testcases import EngineTestCase
from engine_modules.influence.models import BuyInfluenceOrder


class TasksTest(EngineTestCase):
	def setUp(self):
		super(TasksTest, self).setUp()
		self.o = BuyInfluenceOrder(
			player=self.p
		)
		self.o.save()

	def test_task_applied(self):
		"""
		The new player should have influence of 1 after turn resolution
		"""
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).influence.level, 2)

	def test_task_applied_once(self):
		self.g.current_turn += 1
		self.g.save()

		# Check order is only applied on creation turn
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).influence.level, 1)
