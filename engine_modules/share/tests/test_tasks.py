from engine.testcases import EngineTestCase
from engine_modules.share.models import Share, BuyShareOrder
from engine_modules.share.tasks import DividendTask


class TasksTest(EngineTestCase):
	def setUp(self):
		super(TasksTest, self).setUp()

		self.c.assets = 20
		self.c.save()
		self.first_corporation = self.c

		self.c2.assets = 10
		self.c2.save()
		self.medium_corporation = self.c2

		self.c3.assets = 5
		self.c3.save()
		self.last_corporation = self.c3

	def test_buy_task_applied(self):
		"""
		The player should get dividend for previous share, and this turn order should be resolved
		"""
		o = BuyShareOrder(
			player=self.p,
			corporation=self.last_corporation
		)
		o.save()

		self.g.resolve_current_turn()

		s = Share.objects.all()
		self.assertEqual(len(s), 1)
		s = s[0]
		self.assertEqual(s.player, self.p)
		self.assertEqual(s.corporation, self.last_corporation)
		self.assertEqual(s.turn, self.g.current_turn - 1)

	def test_dividend_task_applied_medium_corporation(self):
		"""
		The player should get dividend for previous shares
		"""
		s = Share(
			player=self.p,
			corporation=self.medium_corporation
		)
		s.save()

		money = self.reload(self.p).money
		self.g.resolve_current_turn()

		# We expect dividend on this share
		expected = money + DividendTask.SHARE_BASE_VALUE * self.reload(self.medium_corporation).assets

		self.assertEqual(self.reload(self.p).money, int(expected))

	def test_dividend_task_applied_first_corporation(self):
		"""
		The player should get dividend for previous shares, with bonus if corporation is first
		"""
		s = Share(
			player=self.p,
			corporation=self.first_corporation
		)
		s.save()

		money = self.reload(self.p).money
		self.g.resolve_current_turn()

		# We expect dividend on this share, taking into account the fact that this corporation is the first.
		expected = money + DividendTask.SHARE_BASE_VALUE * self.reload(self.first_corporation).assets * DividendTask.FIRST_BONUS

		self.assertEqual(self.reload(self.p).money, int(expected))

	def test_dividend_task_applied_last_corporation(self):
		"""
		The player should get dividend for previous shares, with malus if corporation is last
		"""
		s = Share(
			player=self.p,
			corporation=self.last_corporation
		)
		s.save()

		money = self.reload(self.p).money

		self.g.resolve_current_turn()
		# We expect dividend on this share, taking into account the fact that this corporation is the last.
		expected = money + DividendTask.SHARE_BASE_VALUE * self.reload(self.last_corporation).assets * DividendTask.LAST_BONUS

		self.assertEqual(self.reload(self.p).money, int(expected))

	def test_complex_dividend_task(self):
		"""
		The player should get dividend for previous shares, with malus if corporation is last
		"""
		s = Share(
			player=self.p,
			corporation=self.medium_corporation
		)
		s.save()
		s2 = Share(
			player=self.p,
			corporation=self.medium_corporation
		)
		s2.save()
		s3 = Share(
			player=self.p,
			corporation=self.medium_corporation
		)
		s3.save()

		money = self.reload(self.p).money

		self.g.resolve_current_turn()
		# We expect dividend on all shares
		expected = money + 3 * DividendTask.SHARE_BASE_VALUE * self.reload(self.medium_corporation).assets

		self.assertEqual(self.reload(self.p).money, int(expected))
