from engine.testcases import EngineTestCase
from engine_modules.influence.orders import BuyInfluenceOrder


class TasksTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		super(TasksTest, self).setUp()
		self.o = BuyInfluenceOrder(
			player=self.p
		)
		self.o.save()

	def test_tasks_applied(self):
		"""
		The new player should have influence of 1 after turn resolution
		"""
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).influence.level, 2)

		# Check order is only applied on current turn
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).influence.level, 2)
