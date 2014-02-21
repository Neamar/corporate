# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder


class RunOrdersTest(EngineTestCase):
	def setUp(self):
		super(RunOrdersTest, self).setUp()

		self.g.disable_invisible_hand = True

	def set_to_zero(self, corporation):
		"""
		Set corporation protection values to 0, to ease testing.
		"""
		bc = corporation.base_corporation
		self._values = (bc.extraction, bc.sabotage, bc.datasteal)

		bc.extraction = bc.sabotage = bc.datasteal = 0

	def set_to_original(self, corporation):
		"""
		Set corporation protection values back to original values, to ease testing.
		"""
		bc = corporation.base_corporation
		bc.extraction = self._values[0]
		bc.sabotage = self._values[0]
		bc.datasteal = self._values[0]


class OffensiveRunOrderTest(RunOrdersTest):
	def test_get_success_probability(self):
		self.p.money = 12465135165465186
		self.p.save()

		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=5,
		)
		self.dso.clean()
		self.dso.save()

		self.dso2 = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=6,
		)
		self.dso2.clean()
		self.dso2.save()

		self.dso3 = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=7,
		)
		self.dso3.clean()
		self.dso3.save()

		self.assertEqual(self.dso.get_success_probability(), 30 + DataStealOrder.PROBA_SUCCESS)
		self.assertEqual(self.dso2.get_success_probability(), 50 + DataStealOrder.PROBA_SUCCESS)

	def test_repay(self):
		self.p.money = 10000
		self.p.save()

		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=1,
			hidden_percents=-4
		)
		self.dso.clean()
		self.dso.save()
		self.dso.resolve()

		self.assertEqual(self.reload(self.p).money, 10000 - 25)

	def test_is_detected(self):
		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=7,
		)
		self.dso.clean()
		self.dso.save()

		self.dso.target_corporation.base_corporation.detection = 0
		self.assertFalse(self.dso.is_detected())

		self.dso.target_corporation.base_corporation.detection = 100
		self.assertTrue(self.dso.is_detected())

	def test_is_protected(self):
		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=7,
		)
		self.dso.clean()
		self.dso.save()

		self.dso.target_corporation.base_corporation.datasteal = 0
		self.assertFalse(self.dso.is_protected())

		self.dso.target_corporation.base_corporation.datasteal = 100
		self.assertTrue(self.dso.is_protected())


class DatastealRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(DatastealRunOrderTest, self).setUp()
		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=0,
		)
		self.dso.clean()
		self.dso.save()

		self.set_to_zero(self.dso.target_corporation)

	def tearDown(self):
		self.set_to_original(self.dso.target_corporation)

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


class SabotageRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(SabotageRunOrderTest, self).setUp()
		self.so = SabotageOrder(
			player=self.p,
			target_corporation=self.c,
			additional_percents=0,
		)
		self.so.clean()
		self.so.save()

		self.set_to_zero(self.so.target_corporation)

	def tearDown(self):
		self.set_to_original(self.so.target_corporation)

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

		begin_assets = self.so.target_corporation.assets

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


class ExtractionRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(ExtractionRunOrderTest, self).setUp()

		self.eo = ExtractionOrder(
			player=self.p,
			target_corporation=self.c,
			kidnapper_corporation=self.c2
		)
		self.eo.clean()
		self.eo.save()

		self.set_to_zero(self.eo.target_corporation)

	def tearDown(self):
		self.set_to_original(self.eo.target_corporation)

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
	def setUp(self):
		super(DefensiveRunOrderTest, self).setUp()
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

		self.set_to_zero(self.so.target_corporation)

	def tearDown(self):
		self.set_to_original(self.so.target_corporation)

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
