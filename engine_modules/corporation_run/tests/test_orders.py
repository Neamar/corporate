# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder


class RunOrdersTest(EngineTestCase):
	def setUp(self):

		super(RunOrdersTest, self).setUp()

		self.c2 = self.g.corporation_set.get(base_corporation_slug="renraku")
		self.c3 = self.g.corporation_set.get(base_corporation_slug="ares")

		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=0,
		)
		self.dso.clean()
		self.dso.save()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation=self.c,
			additional_percents=0,
		)
		self.so.clean()
		self.so.save()

		self.eo = ExtractionOrder(
			player=self.p,
			target_corporation=self.c,
			kidnapper_corporation=self.c2
		)
		self.eo.clean()
		self.eo.save()

		# Refill money for the player
		self.INITIAL_MONEY = 100000
		self.p.money = self.INITIAL_MONEY
		self.p.save()

		self.g.disable_invisible_hand = True

		self.so_initial_extraction = self.so.target_corporation.base_corporation.extraction
		self.so_initial_sabotage = self.so.target_corporation.base_corporation.sabotage
		self.so_initial_datasteal = self.so.target_corporation.base_corporation.datasteal

		self.eo_initial_extraction = self.so.target_corporation.base_corporation.extraction
		self.eo_initial_sabotage = self.so.target_corporation.base_corporation.sabotage
		self.eo_initial_datasteal = self.so.target_corporation.base_corporation.datasteal

		self.dso_initial_extraction = self.so.target_corporation.base_corporation.extraction
		self.dso_initial_sabotage = self.so.target_corporation.base_corporation.sabotage
		self.dso_initial_datasteal = self.so.target_corporation.base_corporation.datasteal

		self.so.target_corporation.base_corporation.extraction = 0
		self.so.target_corporation.base_corporation.sabotage = 0
		self.so.target_corporation.base_corporation.datasteal = 0

		self.eo.target_corporation.base_corporation.extraction = 0
		self.eo.target_corporation.base_corporation.sabotage = 0
		self.eo.target_corporation.base_corporation.datasteal = 0

		self.dso.target_corporation.base_corporation.extraction = 0
		self.dso.target_corporation.base_corporation.sabotage = 0
		self.dso.target_corporation.base_corporation.datasteal = 0

	def tearDown(self):
		self.so.target_corporation.base_corporation.extraction = self.so_initial_extraction
		self.so.target_corporation.base_corporation.sabotage = self.so_initial_sabotage
		self.so.target_corporation.base_corporation.datasteal = self.so_initial_datasteal

		self.eo.target_corporation.base_corporation.extraction = self.so_initial_extraction
		self.eo.target_corporation.base_corporation.sabotage = self.so_initial_sabotage
		self.eo.target_corporation.base_corporation.datasteal = self.so_initial_datasteal

		self.dso.target_corporation.base_corporation.extraction = self.so_initial_extraction
		self.dso.target_corporation.base_corporation.sabotage = self.so_initial_sabotage
		self.dso.target_corporation.base_corporation.datasteal = self.so_initial_datasteal


class OffensiveRunOrderTest(RunOrdersTest):
	def test_datasteal_success(self):
		"""
		Datasteal benefits the stealer 1 asset without costing the stolen
		"""
		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets
		self.dso.additional_percents = 10
		self.dso.save()

		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)

	def test_datasteal_failure(self):
		"""
		Failed datasteal should not change corporation assets.
		"""
		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.dso.additional_percents = 0
		self.dso.hidden_percents = -3
		self.dso.save()
		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)

	def test_datasteal_interception(self):
		"""
		Intercepted datasteal should not change corporation assets.
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.DATASTEAL
		)
		po.clean()
		po.save()

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets
		po.additional_percents = 10
		po.save()

		self.dso.additional_percents = 10
		self.dso.save()
		self.dso.resolve()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)

	def test_datasteal_capture(self):
		"""
		Captured datasteal should not change corporation assets.
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.DATASTEAL,
			hidden_percents=10
		)
		po.clean()
		po.save()

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.dso.additional_percents = 0
		self.dso.hidden_percents = -3
		self.dso.save()
		self.dso.resolve()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)

	def test_sabotage_success(self):
		"""
		Sabotage doesn't benefit anyone, but costs the sabotaged 2 assets
		"""
		begin_assets = self.so.target_corporation.assets

		self.so.additional_percents = 10
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets - 2)

	def test_sabotage_failure(self):
		"""
		Failed sabotage does not change corporation assets
		"""
		begin_assets = self.so.target_corporation.assets

		self.so.additional_percents = 0
		self.so.hidden_percents = -3
		self.so.save()
		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

	def test_sabotage_interception(self):
		"""
		Intercepted sabotage does not change corporation assets
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.SABOTAGE,
			hidden_percents=10,
		)
		po.clean()
		po.save()

		begin_assets = self.dso.target_corporation.assets

		self.so.additional_percents = 10
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

	def test_sabotage_capture(self):
		"""
		Captured sabotage does not change corporation assets
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.SABOTAGE,
			hidden_percents=10,
		)
		po.clean()
		po.save()

		begin_assets = self.so.target_corporation.assets

		self.so.additional_percents = 0
		self.so.hidden_percents = -3
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

	def test_extraction_success(self):
		"""
		Extraction doesn't benefit anyone, but costs the sabotaged 2 assets
		"""
		begin_assets_target = self.eo.target_corporation.assets
		begin_assets_kidnapper = self.eo.kidnapper_corporation.assets

		self.eo.additional_percents = 10
		self.eo.save()
		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets_target - 1)
		self.assertEqual(self.reload(self.eo.kidnapper_corporation).assets, begin_assets_kidnapper + 1)

	def test_extraction_failure(self):
		"""
		Failed extraction does not change corporation assets
		"""
		begin_assets = self.eo.target_corporation.assets

		self.eo.additional_percents = 0
		self.eo.hidden_percents = -3
		self.eo.save()
		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets)

	def test_extraction_interception(self):
		"""
		Intercepted extraction does not change corporation assets
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.EXTRACTION,
			hidden_percents=10,
		)
		po.clean()
		po.save()

		begin_assets = self.eo.target_corporation.assets

		self.eo.additional_percents = 10
		self.eo.save()

		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets)

	def test_extraction_capture(self):
		"""
		Captured extraction does not change corporation assets
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.EXTRACTION,
			hidden_percents=10,
		)
		po.clean()
		po.save()

		begin_assets = self.eo.target_corporation.assets

		self.eo.additional_percents = 0
		self.eo.hidden_percents = -3
		self.eo.save()

		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets)


class DefensiveRunOrderTest(RunOrdersTest):
	def test_offensive_protection_offensive(self):
		"""
		Test that the Protection only cancels one Offensive run
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.SABOTAGE,
			hidden_percents=10,
		)
		po.clean()
		po.save()

		begin_assets = self.so.target_corporation.assets

		self.so.additional_percents = 10
		self.so.save()

		# Should be intercepted
		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

	def test_corpo_can_def_alone(self):
		"""
		Corporations can def themselves
		"""
		self.dso.target_corporation.base_corporation.datasteal = 100

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.dso.additional_percents = 10
		self.dso.save()
		self.dso.resolve()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)
