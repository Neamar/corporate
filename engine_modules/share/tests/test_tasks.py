from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation
from engine_modules.share.models import Share
from engine_modules.share.orders import BuyShareOrder
from engine_modules.share.tasks import DividendTask


class TasksTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless")
		self.bc.save()

		super(TasksTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation=self.bc)
		

	def test_buy_task_applied(self):
		"""
		The player should get dividend for previous share, and this turn order should be resolved
		"""
		self.o = BuyShareOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.save()


	def test_dividend_task_applied(self):
		"""
		The player should get dividend for previous shares
		"""
		# We have one share
		self.s = Share(
			player=self.p,
			corporation=self.c
		)
		self.s.save()

		self.g.current_turn = 5
		self.g.save()

		self.g.resolve_current_turn()
		# We expect dividend on this share, taking into account the fact that this corporation is both first and last.
		expected = self.initial_money + DividendTask.SHARE_BASE_VALUE * self.reload(self.c).assets * 1.25 * 0.75

		self.assertEqual(self.reload(self.p).money, int(expected))
