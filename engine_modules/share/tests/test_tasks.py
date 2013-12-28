from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation
from engine_modules.share.models import Share, BuyShareOrder
from engine_modules.share.tasks import DividendTask


class TasksTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless")
		self.bc.save()
		self.bc2 = BaseCorporation(name="Renraku", description="Priceless")
		self.bc2.save()
		self.bc3 = BaseCorporation(name="Ares", description="Ruthless")
		self.bc3.save()

		super(TasksTest, self).setUp()

		self.last_corporation = self.g.corporation_set.get(base_corporation=self.bc)
		self.last_corporation.assets -= 3
		self.last_corporation.save()

		self.medium_corporation = self.g.corporation_set.get(base_corporation=self.bc2)
		
		self.first_corporation = self.g.corporation_set.get(base_corporation=self.bc3)
		self.first_corporation.assets += 3
		self.first_corporation.save()

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

		self.assertEqual(len(Share.objects.all()), 1)
		self.assertEqual(Share.objects.get(pk=1).player, self.p)
		self.assertEqual(Share.objects.get(pk=1).corporation, self.last_corporation)
		self.assertEqual(Share.objects.get(pk=1).turn, self.g.current_turn - 1)


	def test_dividend_task_applied_medium_corporation(self):
		"""
		The player should get dividend for previous shares
		"""
		# We have one share
		self.s = Share(
			player=self.p,
			corporation=self.medium_corporation
		)
		self.s.save()
		self.g.current_turn = 5
		self.g.save()

		self.g.resolve_current_turn()

		# We expect dividend on this share
		expected = self.initial_money + DividendTask.SHARE_BASE_VALUE * self.reload(self.medium_corporation).assets

		self.assertEqual(self.reload(self.p).money, int(expected))

	def test_dividend_task_applied_first_corporation(self):
		"""
		The player should get dividend for previous shares, with bonus if corporation is first
		"""
		# We have one share
		self.s = Share(
			player=self.p,
			corporation=self.first_corporation
		)
		self.s.save()

		self.g.current_turn = 5
		self.g.save()

		self.g.resolve_current_turn()
		# We expect dividend on this share, taking into account the fact that this corporation is the first.
		expected = self.initial_money + DividendTask.SHARE_BASE_VALUE * self.reload(self.first_corporation).assets * DividendTask.FIRST_BONUS

		self.assertEqual(self.reload(self.p).money, int(expected))


	def test_dividend_task_applied_last_corporation(self):
		"""
		The player should get dividend for previous shares, with malus if corporation is last
		"""
		# We have one share
		self.s = Share(
			player=self.p,
			corporation=self.last_corporation
		)
		self.s.save()

		self.g.current_turn = 5
		self.g.save()

		self.g.resolve_current_turn()
		# We expect dividend on this share, taking into account the fact that this corporation is the last.
		expected = self.initial_money + DividendTask.SHARE_BASE_VALUE * self.reload(self.last_corporation).assets * DividendTask.LAST_BONUS

		self.assertEqual(self.reload(self.p).money, int(expected))

	def test_dividend_task_applied_medium_corporation_citizenship(self):
		"""
		The player should get more dividend for being a citizen of the corporation
		"""
		# We have one share
		self.s = Share(
			player=self.p,
			corporation=self.medium_corporation
		)
		self.s.save()
		self.p.citizenship.corporation = self.medium_corporation
		self.p.citizenship.save()

		self.g.current_turn = 5
		self.g.save()

		self.g.resolve_current_turn()

		# We expect dividend on this share, taking into account the fact that we are citizen from this corporation
		expected = self.initial_money + DividendTask.SHARE_BASE_VALUE * self.reload(self.medium_corporation).assets * DividendTask.CITIZENSHIP_BONUS

		self.assertEqual(self.reload(self.p).money, int(expected))
