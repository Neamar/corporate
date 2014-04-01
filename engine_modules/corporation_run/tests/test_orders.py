# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder
from engine_modules.corporation.testcases import override_base_corporations


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
		Check raw probability values (without timing malus)
		"""
		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=1,
			hidden_percents=3
		)

		self.assertEqual(dso.get_raw_probability(), dso.additional_percents * 10 + dso.hidden_percents * 10 + dso.BASE_SUCCESS_PROBABILITY)

	def test_get_success_probability_with_timing_malus(self):
		"""
		Test for the timing malus (multiple runs, same type)
		"""
		self.p.money = 20000
		self.p.save()

		def create_order(additional_percents):
			dso = DataStealOrder(
				stealer_corporation=self.c2,
				player=self.p,
				target_corporation=self.c,
				additional_percents=additional_percents,
			)
			dso.save()
			return dso

		dso = create_order(5)
		dso2 = create_order(6)
		dso3 = create_order(6)
		dso4 = create_order(7)

		# -30 : three similar runs above
		self.assertEqual(dso.get_success_probability(), dso.additional_percents * 10 - 30 + DataStealOrder.BASE_SUCCESS_PROBABILITY)

		# -20 : two similar runs above or equal
		self.assertEqual(dso2.get_success_probability(), dso2.additional_percents * 10 - 20 + DataStealOrder.BASE_SUCCESS_PROBABILITY)
		self.assertEqual(dso3.get_success_probability(), dso3.additional_percents * 10 - 20 + DataStealOrder.BASE_SUCCESS_PROBABILITY)

		# No malus
		self.assertEqual(dso4.get_success_probability(), dso4.additional_percents * 10 + DataStealOrder.BASE_SUCCESS_PROBABILITY)

	def test_repay(self):
		"""
		Player gets back half the money when the run fails
		"""
		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=1,
			hidden_percents=-10
		)
		dso.save()
		dso.resolve()

		self.assertEqual(self.reload(self.p).money, self.initial_money - dso.get_cost() / 2)

	@override_base_corporations
	def test_is_detected(self):
		"""
		Check detection use corporation base values
		"""
		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=7,
		)
		dso.save()

		dso.target_corporation.base_corporation.detection = 0
		self.assertFalse(dso.is_detected())

		dso.target_corporation.base_corporation.detection = 100
		self.assertTrue(dso.is_detected())

	@override_base_corporations
	def test_is_protected(self):
		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=7,
		)
		dso.save()

		dso.target_corporation.base_corporation.datasteal = 0
		self.assertFalse(dso.is_protected())

		dso.target_corporation.base_corporation.datasteal = 100
		self.assertTrue(dso.is_protected())

	def test_get_protection_values(self):
		"""
		Protection values should include Protection runs.
		"""
		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=7,
		)
		dso.save()

		self.assertEqual(dso.get_protection_values(), [dso.target_corporation.base_corporation.datasteal])

		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.DATASTEAL,
			hidden_percents=10,
		)
		po.save()

		self.assertEqual(dso.get_protection_values(), [po.get_success_probability(), dso.target_corporation.base_corporation.datasteal])

	@override_base_corporations
	def test_detected_create_newsfeed(self):
		"""
		Check detection use corporation base values
		"""
		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=7,
		)
		dso.save()

		dso.target_corporation.base_corporation.detection = 100

		dso.resolve()

		previous_message=self.g.newsfeed_set.get().content
		self.assertIn('Shiawase', self.g.newsfeed_set.get().content) #test bon fichier
		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=7,
		)
		dso.save()

		dso.target_corporation.base_corporation.detection = 100

		dso.resolve()
		self.assertEqual(previous_message, self.g.newsfeed_set.last().content) # test si premier message différent du deuxième

		a = 0
		while a < 4:
			a += 1
			self.p.money=2000
			previous_message=self.g.newsfeed_set.last().content
			self.assertIn('Shiawase', self.g.newsfeed_set.last().content)
			dso = DataStealOrder(
				stealer_corporation=self.c2,
				player=self.p,
				target_corporation=self.c,
				additional_percents=7,
			)
			dso.save()

			dso.target_corporation.base_corporation.detection = 100

			dso.resolve()
		self.maxDiff=None
		self.assertEqual(previous_message, self.g.newsfeed_set.last().content) #test butoir

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

		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
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
		self.so.hidden_percents = -10
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

	def test_sabotage_interception(self):
		"""
		Intercepted sabotage does not change corporation assets
		"""
		begin_assets = self.so.target_corporation.assets

		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
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
		begin_assets_target = self.eo.target_corporation.assets
		begin_assets_kidnapper = self.eo.kidnapper_corporation.assets

		self.eo.additional_percents = 0
		self.eo.hidden_percents = -10
		self.eo.save()

		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets_target)
		self.assertEqual(self.reload(self.eo.kidnapper_corporation).assets, begin_assets_kidnapper)

	def test_extraction_interception(self):
		"""
		Intercepted extraction does not change corporation assets
		"""
		begin_assets_target = self.eo.target_corporation.assets
		begin_assets_kidnapper = self.eo.kidnapper_corporation.assets

		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.EXTRACTION,
			hidden_percents=10,
		)
		po.save()

		self.eo.additional_percents = 10
		self.eo.save()

		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets_target)
		self.assertEqual(self.reload(self.eo.kidnapper_corporation).assets, begin_assets_kidnapper)


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

	def test_has_base_value(self):
		"""
		Protection has defaut protection values
		"""

		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.DATASTEAL,
			additional_percents=1,
		)
		po.save()

		self.assertEqual(po.get_success_probability(), po.additional_percents * 10 + po.BASE_SUCCESS_PROBABILITY[po.defense])

	@override_base_corporations
	def test_corpo_can_protect_alone(self):
		"""
		Corporations can protect themselves
		"""
		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.dso.target_corporation.base_corporation.datasteal = 100

		self.dso.additional_percents = 10
		self.dso.save()

		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)
