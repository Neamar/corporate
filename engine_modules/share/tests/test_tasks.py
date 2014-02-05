from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation
from engine_modules.share.models import Share, BuyShareOrder
from engine_modules.share.tasks import DividendTask


class TasksTest(EngineTestCase):
	def setUp(self):
		super(TasksTest, self).setUp()

		self.g.corporation_set.all().delete()

		self.first_corporation = Corporation(base_corporation_slug='renraku', assets=20)
		self.g.corporation_set.add(self.first_corporation)
		self.medium_corporation = Corporation(base_corporation_slug='shiawase', assets=10)
		self.g.corporation_set.add(self.medium_corporation)
		self.last_corporation = Corporation(base_corporation_slug='ares', assets=5)
		self.g.corporation_set.add(self.last_corporation)

		self.g.disable_invisible_hand = True

	def test_buy_task_applied(self):
		"""
		The player should get dividend for previous share, and this turn order should be resolved
		"""
		self.o = BuyShareOrder(
			player=self.p,
			corporation=self.last_corporation
		)
		self.o.save()

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
		self.s = Share(
			player=self.p,
			corporation=self.medium_corporation
		)
		self.s.save()

		money = self.reload(self.p).money
		self.g.resolve_current_turn()

		# We expect dividend on this share
		expected = money + DividendTask.SHARE_BASE_VALUE * self.reload(self.medium_corporation).assets

		self.assertEqual(self.reload(self.p).money, int(expected))

	def test_dividend_task_applied_first_corporation(self):
		"""
		The player should get dividend for previous shares, with bonus if corporation is first
		"""
		self.s = Share(
			player=self.p,
			corporation=self.first_corporation
		)
		self.s.save()

		money = self.reload(self.p).money
		self.g.resolve_current_turn()

		# We expect dividend on this share, taking into account the fact that this corporation is the first.
		expected = money + DividendTask.SHARE_BASE_VALUE * self.reload(self.first_corporation).assets * DividendTask.FIRST_BONUS

		self.assertEqual(self.reload(self.p).money, int(expected))

	def test_dividend_task_applied_last_corporation(self):
		"""
		The player should get dividend for previous shares, with malus if corporation is last
		"""
		self.s = Share(
			player=self.p,
			corporation=self.last_corporation
		)
		self.s.save()

		money = self.reload(self.p).money

		self.g.resolve_current_turn()
		# We expect dividend on this share, taking into account the fact that this corporation is the last.
		expected = money + DividendTask.SHARE_BASE_VALUE * self.reload(self.last_corporation).assets * DividendTask.LAST_BONUS

		self.assertEqual(self.reload(self.p).money, int(expected))

	def test_no_immediate_dividend_after_turn_1(self):
		"""
		The player should not get dividends for shares he just bought, except in turn 1
		"""
		# Skip first turn
		self.g.resolve_current_turn()

		self.s = Share(
			player=self.p,
			corporation=self.medium_corporation
		)
		self.s.save()

		money = self.reload(self.p).money
		self.g.resolve_current_turn()

		# No dividends
		self.assertEqual(self.reload(self.p).money, money)

	def test_immediate_dividend_on_turn_1(self):
		"""
		The player should get dividends for shares he just bought in turn 1
		"""
		self.s = Share(
			player=self.p,
			corporation=self.medium_corporation
		)
		self.s.save()

		money = self.reload(self.p).money
		self.g.resolve_current_turn()

		# No dividends
		self.assertEqual(self.reload(self.p).money, money + DividendTask.SHARE_BASE_VALUE * self.reload(self.medium_corporation).assets)
