from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.share.models import Share
from engine_modules.detroit_inc.models import DIncVoteOrder
from engine_modules.corporation_run.models import DataStealOrder


class DIncPartyLineTest(EngineTestCase):
	def setUp(self):
		"""
		p is top shareholder in c,
		p2 is top shareholder in c2,
		p3 is top shareholder in c3,
		"""
		super(DIncPartyLineTest, self).setUp()

		self.p2 = Player(game=self.g)
		self.p2.save()

		self.p3 = Player(game=self.g, )
		self.p3.save()

		self.s = Share(
			corporation=self.c,
			player=self.p,
			turn=self.g.current_turn
		)
		self.s.save()

		self.s2 = Share(
			corporation=self.c2,
			player=self.p2,
			turn=self.g.current_turn
		)
		self.s2.save()

		self.s3 = Share(
			corporation=self.c3,
			player=self.p3,
			turn=self.g.current_turn
		)
		self.s3.save()

	def set_turn_line(self, L1, L2, L3):
		"""
		A little helper to set the Line each player has voted for this turn
		"""

		v = DIncVoteOrder(
			player=self.p,
			coalition=L1
		)
		v.save()

		v2 = DIncVoteOrder(
			player=self.p2,
			coalition=L2
		)
		v2.save()

		v3 = DIncVoteOrder(
			player=self.p3,
			coalition=L3
		)
		v3.save()

	def test_dinc_CPUB_line_effects(self):
		"""
		Test what happens when the CPUB party line is chosen
		"""

		initial_assets = self.c.assets
		initial_assets2 = self.c2.assets
		initial_assets3 = self.c3.assets

		self.set_turn_line(DIncVoteOrder.CPUB, DIncVoteOrder.CPUB, DIncVoteOrder.RSEC)

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, initial_assets + 1)
		self.assertEqual(self.reload(self.c2).assets, initial_assets2 + 1)
		self.assertEqual(self.reload(self.c3).assets, initial_assets3 - 1)

	def test_dinc_RSEC_line_effects(self):
		"""
		Test what happens when the RSEC party line is chosen
		"""

		self.set_turn_line(DIncVoteOrder.CONS, DIncVoteOrder.RSEC, DIncVoteOrder.RSEC)
		self.g.resolve_current_turn()

		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p2,
			target_corporation_market=self.c.corporation_markets.first(),
			additional_percents=5,
		)
		dso.save()

		# Reduction on first run
		self.assertEqual(dso.get_cost(), dso.LAUNCH_COST + dso.BASE_COST * dso.additional_percents - dso.INFLUENCE_BONUS)

		dso2 = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p2,
			target_corporation_market=self.c.corporation_markets.first(),
			additional_percents=5,
		)
		dso2.save()

		# No reduction on second run
		self.assertEqual(dso2.get_cost(), dso2.LAUNCH_COST + dso2.BASE_COST * dso2.additional_percents)

	def test_dinc_RSEC_last_turn(self):
		"""
		Should not reduce price of a run
		"""
		while self.g.current_turn < self.g.total_turn - 1:
			self.g.resolve_current_turn()
		self.set_turn_line(DIncVoteOrder.CONS, DIncVoteOrder.RSEC, DIncVoteOrder.RSEC)
		self.g.resolve_current_turn()

		dso3 = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p2,
			target_corporation_market=self.c.corporation_markets.first(),
			additional_percents=5,
		)
		dso3.save()

		# Reduction on first run
		self.assertEqual(dso3.get_cost(), dso3.LAUNCH_COST + dso3.BASE_COST * dso3.additional_percents)
