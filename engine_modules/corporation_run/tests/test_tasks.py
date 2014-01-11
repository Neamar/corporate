from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder
from engine_modules.corporation.models import BaseCorporation
from engine_modules.corporation_run.tasks import OffensiveRunTask


class OffensiveRunTaskTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless")
		self.bc.save()
		self.bc2 = BaseCorporation(name="Renraku", description="Priceless")
		self.bc2.save()
		self.bc3 = BaseCorporation(name="Ares", description="Ruthless")
		self.bc3.save()

		super(OffensiveRunTaskTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation=self.bc)
		self.c.assets = 10
		self.c.save()

		self.c2 = self.g.corporation_set.get(base_corporation=self.bc2)
		self.c2.assets = 15
		self.c2.save()

		self.c3 = self.g.corporation_set.get(base_corporation=self.bc3)
		self.c3.assets = 20
		self.c3.save()

		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c
		)
		self.dso.clean()
		self.dso.save()

		self.po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c
		)
		self.po.clean()
		self.po.save()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation = self.c
		)
		self.so.clean()
		self.so.save()

		# Refill money for the player
		self.p.money = 100000
		self.p.save()

		self.g.disable_invisible_hand = True

	def test_offensive_run_task(self):
		"""
		Check the task solves the run
		"""
		begin_sabotaged_assets = self.so.target_corporation.assets

		self.so.additional_percents = 10
		self.so.save()

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_sabotaged_assets - 2)


	def test_offensive_runs_task_descending_probability(self):
		"""
		Test that Offensive Runs are resolved from highest to lowest success probability
		In this case, the Datasteal with 200 should be the one that fails (because of 
		the Protection) and the Sabotage with 100 should succeed
		"""

		begin_stealer_assets = self.dso.stealer_corporation.assets
		begin_sabotaged_assets = self.so.target_corporation.assets

		self.po.additional_percents = 10
		self.po.save()
		self.dso.additional_percents = 20
		self.dso.save()
		self.so.additional_percents = 10
		self.so.save()

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_stealer_assets)
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_sabotaged_assets - 2)

	def test_datasteal_protection_datasteal_datasteal(self):
		"""
		Functional test, the first DataSteal fails because of the Protection, so the second should succeed and benefit the client while the third succeeds without benefits
		"""

		self.po.additional_percents = 10
		self.po.save()
		self.dso.additional_percents = 20
		self.dso.save()
		dso2 = DataStealOrder(
			stealer_corporation=self.c3,
			player=self.p,
			target_corporation=self.c,
			additional_percents=15
		)
		dso2.save()
		dso3 = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=10
		)
		dso3.save()

		begin_assets_stealer1 = self.dso.stealer_corporation.assets
		begin_assets_stealer2 = dso2.stealer_corporation.assets
		begin_assets_stealer3 = dso3.stealer_corporation.assets

		self.g.resolve_current_turn()

		# protected
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer1)
		# succeeded
		self.assertEqual(self.reload(dso2.stealer_corporation).assets, begin_assets_stealer2 + 1)
		# already stolen
		self.assertEqual(self.reload(dso3.stealer_corporation).assets, begin_assets_stealer3)
