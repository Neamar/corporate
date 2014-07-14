from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import ProtectionOrder, SabotageOrder


class OffensiveRunTaskTest(EngineTestCase):
	def setUp(self):

		super(OffensiveRunTaskTest, self).setUp()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation=self.c,
			target_corporation_market=self.c.corporationmarket_set.get(market__name=self.c.historic_market.name),
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
		And that only the first one has been resolved
		"""

		begin_sabotaged_assets = self.so.target_corporation.assets

		so2 = SabotageOrder(
                        player=self.p,
                        target_corporation=self.c2,
			target_corporation_market=self.c2.corporationmarket_set.get(market__name=self.c2.historic_market.name),
                        additional_percents=4,
                )
		
		so2.clean()
		so2.save()
		begin_sabotaged_assets_2 = so2.target_corporation.assets

		so3 = SabotageOrder(
                        player=self.p,
                        target_corporation=self.c3,
			target_corporation_market=self.c3.corporationmarket_set.get(market__name=self.c3.historic_market.name),
                        additional_percents=8,
                )
		
		so3.clean()
		so3.save()
		begin_sabotaged_assets_3 = so3.target_corporation.assets

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_sabotaged_assets)
		self.assertEqual(self.reload(so2.target_corporation).assets, begin_sabotaged_assets_2)
		self.assertEqual(self.reload(so3.target_corporation).assets, begin_sabotaged_assets_3 - 2)
