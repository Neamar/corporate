from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import SabotageOrder, ExtractionOrder


class OffensiveRunTaskTest(EngineTestCase):
	def setUp(self):

		super(OffensiveRunTaskTest, self).setUp()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation_market=self.c.get_random_corporation_market(),
			additional_percents=0,
		)
		self.so.clean()
		self.so.save()

		# Refill money for the player
		self.INITIAL_MONEY = 100000
		self.p.money = self.INITIAL_MONEY
		self.p.save()

		self.so_initial_extraction = self.so.target_corporation.base_corporation.sabotage

	def test_offensive_run_task(self):
		"""
		Check the task solves the run
		"""
		begin_sabotaged_assets = self.so.target_corporation.assets
		self.so.target_corporation.base_corporation.sabotage = 0
		self.so.additional_percents = 10
		self.so.save()

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_sabotaged_assets - 2)

		self.so.target_corporation.base_corporation.sabotage = self.so_initial_extraction

	def test_offensive_resolve_order(self):
		"""
		Check that offensive runs are resolved in order of raw_probability
		And that only the first one has been resolved on the same market
		"""

		# We don't want the setUp order to interfere :
		self.so.delete()

		# We find a common corporationmarket on c with a market shared by c,c2 and c3
		c2_markets = self.c2.markets
		c3_markets = self.c3.markets
		common_corporation_markets = [cm for cm in self.c.corporation_markets if cm.market in c2_markets and cm.market in c3_markets]
		common_corporation_market = common_corporation_markets[0]

		assets_c_before = self.c.assets
		assets_c3_before = self.c3.assets
		assets_c2_before = self.c2.assets

		# We order an extraction run for c2 and c3 on this market
		so2 = ExtractionOrder(
			player=self.p,
			target_corporation_market=common_corporation_market,
			stealer_corporation=self.c2,
			additional_percents=4,
		)

		so2.clean()
		so2.save()
		
		so3 = ExtractionOrder(
			player=self.p,
			target_corporation_market=common_corporation_market,
			stealer_corporation=self.c3,
			additional_percents=8,
		)

		so3.clean()
		so3.save()
		
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, assets_c_before - 1)  # SabotageOrder of the setUp succeeded + 1 ExtractionOrder succeeded
		self.assertEqual(self.reload(self.c2).assets, assets_c3_before)  # ExtractionOrder failed
		self.assertEqual(self.reload(self.c3).assets, assets_c2_before + 1)  # ExtractionOrder succeeded
