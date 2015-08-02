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
			player=self.p,
			target_corporation_market=self.c.corporation_markets.first(),
			additional_percents=5,
		)
		dso.save()

		# 20% bonus
		self.assertEqual(dso.get_raw_probability(), dso.additional_percents * 10 + dso.BASE_SUCCESS_PROBABILITY - 20)

		dso2 = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p2,
			target_corporation_market=self.c.corporation_markets.first(),
			additional_percents=5,
		)
		dso2.save()

		# 20% malus
		self.assertEqual(dso2.get_raw_probability(), dso2.additional_percents * 10 + dso2.BASE_SUCCESS_PROBABILITY + 20)