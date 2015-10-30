# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder
from engine_modules.corporation_run.decorators import override_max_protection


class RunOrdersTest(EngineTestCase):
	pass


class CorporationRunOrderTest(RunOrdersTest):
	def test_get_raw_probability(self):
		"""
		Check raw probability values
		"""

		common_corporation_market = self.c.get_common_corporation_market(self.c2)

		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation_market=common_corporation_market,
			additional_percents=1,
			hidden_percents=3
		)

		self.assertEqual(dso.get_raw_probability(), dso.additional_percents * 10 + dso.hidden_percents * 10 + dso.BASE_SUCCESS_PROBABILITY)


class DatastealRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(DatastealRunOrderTest, self).setUp()

		common_corporation_market = self.c.get_common_corporation_market(self.c2)

		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation_market=common_corporation_market,
			additional_percents=0,
		)
		self.dso.clean()
		self.dso.save()

	def test_datasteal_success(self):
		"""
		Datasteal benefits the stealer 1 asset without costing the stolen
		The 2 corporations must have a common market
		"""
		begin_assets_stealer = self.dso.stealer_corporation.assets

		self.dso.additional_percents = 10
		self.dso.save()

		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)

	def test_datasteal_failure(self):
		"""
		Failed datasteal should not change corporation assets.
		"""
		begin_assets_stealer = self.dso.stealer_corporation.assets

		self.dso.additional_percents = 0
		self.dso.hidden_percents = -10
		self.dso.save()

		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)

	@override_max_protection
	def test_datasteal_interception(self):
		"""
		Intercepted datasteal should not change corporation assets.
		"""
		begin_assets_stealer = self.dso.stealer_corporation.assets

		po = ProtectionOrder(
			player=self.p,
			protected_corporation_market=self.dso.target_corporation_market,
		)
		po.clean()
		po.save()

		po.additional_percents = 10
		po.save()

		self.dso.additional_percents = 10
		self.dso.save()

		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)


class SabotageRunOrderTest(RunOrdersTest):
	def setUp(self):

		super(RunOrdersTest, self).setUp()

		common_corporation_market = self.c.get_common_corporation_market(self.c2)

		super(SabotageRunOrderTest, self).setUp()
		self.so = SabotageOrder(
			player=self.p,
			target_corporation_market=common_corporation_market,
			additional_percents=0,
		)
		self.so.clean()
		self.so.save()

	def test_sabotage_success(self):
		"""
		Sabotage doesn't benefit anyone, but costs the sabotaged 2 assets
		"""
		begin_assets = self.so.target_corporation.assets
		self.so.target_corporation_market.value = 8
		self.so.target_corporation_market.save()
		begin_market_value = self.reload(self.so.target_corporation_market).value

		self.so.additional_percents = 10
		self.so.save()

		self.so.resolve()

		delta = begin_market_value - self.reload(self.so.target_corporation_market).value
		self.assertEqual(delta, 2)
		self.assertEqual(self.so.target_corporation.assets, begin_assets - delta)

	def test_sabotage_failure(self):
		"""
		Failed sabotage does not change corporation assets
		"""
		begin_assets = self.so.target_corporation.assets

		self.so.additional_percents = 0
		self.so.hidden_percents = -10
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

	@override_max_protection
	def test_sabotage_interception(self):
		"""
		Intercepted sabotage does not change corporation assets
		"""
		begin_assets = self.so.target_corporation.assets

		po = ProtectionOrder(
			player=self.p,
			protected_corporation_market=self.so.target_corporation_market,
			hidden_percents=10,
		)
		po.clean()
		po.save()

		self.so.additional_percents = 10
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)


class ExtractionRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(ExtractionRunOrderTest, self).setUp()

		common_corporation_market = self.c.get_common_corporation_market(self.c2)

		self.eo = ExtractionOrder(
			player=self.p,
			target_corporation_market=common_corporation_market,
			stealer_corporation=self.c2
		)
		self.eo.clean()
		self.eo.save()

	def test_extraction_success(self):
		"""
		Extraction benefits the stealer 1 asset and costs the stolen 1
		"""
		begin_assets_target = self.eo.target_corporation.assets
		begin_assets_kidnapper = self.eo.stealer_corporation.assets

		self.eo.additional_percents = 10
		self.eo.save()

		self.eo.resolve()

		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets_target - 1)
		self.assertEqual(self.reload(self.eo.stealer_corporation).assets, begin_assets_kidnapper + 1)

	def test_extraction_failure(self):
		"""
		Failed extraction does not change corporation assets
		"""
		begin_assets_target = self.eo.target_corporation.assets
		begin_assets_kidnapper = self.eo.stealer_corporation.assets

		self.eo.additional_percents = 0
		self.eo.hidden_percents = -10
		self.eo.save()

		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets_target)
		self.assertEqual(self.reload(self.eo.stealer_corporation).assets, begin_assets_kidnapper)

	@override_max_protection
	def test_extraction_interception(self):
		"""
		Intercepted extraction does not change corporation assets
		"""
		begin_assets_target = self.eo.target_corporation.assets
		begin_assets_kidnapper = self.eo.stealer_corporation.assets

		po = ProtectionOrder(
			player=self.p,
			protected_corporation_market=self.eo.target_corporation_market,
			hidden_percents=10,
		)
		po.save()

		self.eo.additional_percents = 10
		self.eo.save()

		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets_target)
		self.assertEqual(self.reload(self.eo.stealer_corporation).assets, begin_assets_kidnapper)


class DefensiveRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(DefensiveRunOrderTest, self).setUp()
		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation_market=self.c.corporationmarket_set.get(market__name=self.c.base_corporation.markets.keys()[0]),
			additional_percents=0,
		)
		self.dso.clean()
		self.dso.save()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation_market=self.dso.target_corporation_market,
			additional_percents=0,
		)
		self.so.clean()
		self.so.save()
