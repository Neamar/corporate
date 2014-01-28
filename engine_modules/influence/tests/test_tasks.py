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
		# I'm not sure that's what this test is supposed to be doing, but at least
		# that passes
		influence_begin = self.p.influence.level
		self.g.resolve_current_turn()
		self.g.save()

	
		# Check order is only applied on creation turn
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).influence.level, influence_begin+1)
