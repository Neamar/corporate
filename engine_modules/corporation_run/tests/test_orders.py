# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder
from django.core.exceptions import ValidationError


class RunOrdersTest(EngineTestCase):
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


class OffensiveCorporationRunOrderTest(RunOrdersTest):
	def test_get_raw_probability(self):
		"""
		Check raw probability values
		"""
		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			target_corporation_market=self.c.corporationmarket_set.get(market=self.c.historic_market),
			additional_percents=1,
			hidden_percents=3
		)

		self.assertEqual(dso.get_raw_probability(), dso.additional_percents * 10 + dso.hidden_percents * 10 + dso.BASE_SUCCESS_PROBABILITY)


class DatastealRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(DatastealRunOrderTest, self).setUp()
		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			# The 3 test corporations have the same 3 first markets
			# Only the last one is different
			target_corporation_market=self.c.corporationmarket_set.get(
				market=self.c.historic_market),
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

	def test_datasteal_interception(self):
		"""
		Intercepted datasteal should not change corporation assets.
		"""
		begin_assets_stealer = self.dso.stealer_corporation.assets

		# Needed to make the datasteal fail unconditionally
		ProtectionOrder.MAX_PERCENTS = 0

		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			target_corporation_market=self.dso.target_corporation_market,
			defense=ProtectionOrder.DATASTEAL
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
		super(SabotageRunOrderTest, self).setUp()
		self.so = SabotageOrder(
			player=self.p,
			target_corporation=self.c,
			target_corporation_market=self.c.corporationmarket_set.get(market=self.c.historic_market),
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
		self.so.target_corporation_market.value = 8
		self.so.target_corporation_market.save()
		begin_market_value = self.reload(self.so.target_corporation_market).value

		self.so.additional_percents = 10
		self.so.save()

		self.so.resolve()

		delta = begin_market_value - self.reload(self.so.target_corporation_market).value
		self.assertEqual(delta, 2)
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets - delta)

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

	def test_sabotage_interception(self):
		"""
		Intercepted sabotage does not change corporation assets
		"""
		begin_assets = self.so.target_corporation.assets

		# Needed to make the sabotage fail unconditionally
		ProtectionOrder.MAX_PERCENTS = 0

		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			target_corporation_market=self.so.target_corporation_market,
			defense=ProtectionOrder.SABOTAGE,
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

		self.eo = ExtractionOrder(
			player=self.p,
			target_corporation=self.c,
			target_corporation_market=self.c.corporationmarket_set.get(market__name=self.c.base_corporation.markets.keys()[0]),
			stealer_corporation=self.c2
		)
		self.eo.clean()
		self.eo.save()

		self.set_to_zero(self.eo.target_corporation)

	def tearDown(self):
		self.set_to_original(self.eo.target_corporation)

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

	def test_extraction_interception(self):
		"""
		Intercepted extraction does not change corporation assets
		"""
		begin_assets_target = self.eo.target_corporation.assets
		begin_assets_kidnapper = self.eo.stealer_corporation.assets

		# Needed to make the extraction fail unconditionally
		ProtectionOrder.MAX_PERCENTS = 0

		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			target_corporation_market=self.eo.target_corporation_market,
			defense=ProtectionOrder.EXTRACTION,
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
			target_corporation=self.c,
			target_corporation_market=self.c.corporationmarket_set.get(market__name=self.c.base_corporation.markets.keys()[0]),
			additional_percents=0,
		)
		self.dso.clean()
		self.dso.save()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation=self.c,
			target_corporation_market=self.dso.target_corporation_market,
			additional_percents=0,
		)
		self.so.clean()
		self.so.save()

		self.set_to_zero(self.so.target_corporation)

	def tearDown(self):
		self.set_to_original(self.so.target_corporation)
