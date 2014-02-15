# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder, datasteal_messages, sabotage_messages, extraction_messages


class RunOrdersTest(EngineTestCase):
	def setUp(self):

		super(RunOrdersTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation_slug="shiawase")
		self.c2 = self.g.corporation_set.get(base_corporation_slug="renraku")
		self.c3 = self.g.corporation_set.get(base_corporation_slug="ares")

		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c
		)
		self.dso.clean()
		self.dso.save()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation=self.c
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

		note = self.dso.player.note_set.get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['success'] % (self.dso.target_corporation.base_corporation.name, self.dso.stealer_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_datasteal_failure(self):
		"""
		Dailed datasteal should not change corporation assets.
		"""

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)

		note = self.dso.player.note_set.get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['fail'] % (self.dso.target_corporation.base_corporation.name, self.dso.stealer_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

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
		self.dso.resolve()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)

		aggressor_note = self.dso.player.note_set.get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['interception']['aggressor'] % (self.dso.target_corporation.base_corporation.name)
		self.assertEqual(aggressor_note.content, expected_message)

		protector_note = po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = datasteal_messages['interception']['protector'] % (self.dso.target_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)

	def test_datasteal_capture(self):
		"""
		Captured datasteal should not change corporation assets.
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
		self.dso.additional_percents = 0
		self.dso.resolve()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)

		aggressor_note = self.dso.player.note_set.get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['capture']['aggressor'] % (self.dso.target_corporation.base_corporation.name)
		self.assertTrue(aggressor_note.content, expected_message)

		protector_note = po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = datasteal_messages['capture']['protector'] % (self.dso.player.name, self.dso.target_corporation.base_corporation.name, self.dso.stealer_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)

	def test_sabotage_success(self):
		"""
		Sabotage doesn't benefit anyone, but costs the sabotaged 2 assets
		"""

		begin_assets = self.so.target_corporation.assets

		self.so.additional_percents = 10
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets - 2)

		note = self.so.player.note_set.get(category=u"Run de Sabotage", turn=self.g.current_turn)
		expected_message = sabotage_messages['success'] % (self.so.target_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_sabotage_failure(self):
		"""
		Failed sabotage does not change corporation assets
		"""

		begin_assets = self.so.target_corporation.assets

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

		note = self.so.player.note_set.get(category=u"Run de Sabotage", turn=self.g.current_turn)
		expected_message = sabotage_messages['fail'] % (self.so.target_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_sabotage_interception(self):
		"""
		Intercepted sabotage does not change corporation assets
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.SABOTAGE
		)
		po.clean()
		po.save()

		begin_assets = self.dso.target_corporation.assets

		po.additional_percents = 10
		po.save()
		self.so.additional_percents = 10

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

		aggressor_note = self.so.player.note_set.get(category=u"Run de Sabotage", turn=self.g.current_turn)
		expected_message = sabotage_messages['interception']['aggressor'] % (self.so.target_corporation.base_corporation.name)
		self.assertEqual(aggressor_note.content, expected_message)

		protector_note = po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = sabotage_messages['interception']['protector'] % (self.so.target_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)

	def test_sabotage_capture(self):
		"""
		Captured sabotage does not change corporation assets
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.SABOTAGE
		)
		po.clean()
		po.save()

		begin_assets = self.so.target_corporation.assets

		po.additional_percents = 10
		po.save()
		self.so.additional_percents = 0
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)
		aggressor_note = self.so.player.note_set.get(category=u"Run de Sabotage", turn=self.g.current_turn)
		expected_message = sabotage_messages['capture']['aggressor'] % (self.so.target_corporation.base_corporation.name)
		self.assertEqual(aggressor_note.content, expected_message)

		protector_note = po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = sabotage_messages['capture']['protector'] % (self.so.player.name, self.so.target_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)

	def test_extraction_success(self):
		"""
		Extraction doesn't benefit anyone, but costs the sabotaged 2 assets
		"""

		begin_assets_target = self.eo.target_corporation.assets
		begin_target_kidnapper = self.eo.kidnapper_corporation.assets
		self.eo.additional_percents = 10
		self.eo.save()

		self.eo.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets_target - 1)
		self.assertEqual(self.reload(self.so.kidnapper_corporation).assets, begin_assets_kidnapper + 1)

		note = self.eo.player.note_set.get(category=u"Run d'Extraction", turn=self.g.current_turn)
		expected_message = extraction_messages['success'] % (self.eo.target_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_extraction_failure(self):
		"""
		Failed extraction does not change corporation assets
		"""

		begin_assets = self.eo.target_corporation.assets

		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets)

		note = self.eo.player.note_set.get(category=u"Run d'Extraction", turn=self.g.current_turn)
		expected_message = extraction_messages['fail'] % (self.eo.target_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_extraction_interception(self):
		"""
		Intercepted extraction does not change corporation assets
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.EXTRACTION
		)
		po.clean()
		po.save()

		begin_assets = self.eo.target_corporation.assets

		po.additional_percents = 10
		po.save()
		self.so.additional_percents = 10

		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets)

		aggressor_note = self.so.player.note_set.get(category=u"Run d'Extraction", turn=self.g.current_turn)
		expected_message = extraction_messages['interception']['aggressor'] % (self.eo.target_corporation.base_corporation.name)
		self.assertEqual(aggressor_note.content, expected_message)

		protector_note = po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = extraction_messages['interception']['protector'] % (self.eo.target_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)

	def test_extraction_capture(self):
		"""
		Captured extraction does not change corporation assets
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.EXTRACTION
		)
		po.clean()
		po.save()

		begin_assets = self.eo.target_corporation.assets

		po.additional_percents = 10
		po.save()
		self.eo.additional_percents = 0
		self.eo.save()

		self.eo.resolve()
		self.assertEqual(self.reload(self.eo.target_corporation).assets, begin_assets)
		aggressor_note = self.eo.player.note_set.get(category=u"Run d'Extraction", turn=self.g.current_turn)
		expected_message = extraction_messages['capture']['aggressor'] % (self.eo.target_corporation.base_corporation.name)
		self.assertEqual(aggressor_note.content, expected_message)

		protector_note = po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = extraction_messages['capture']['protector'] % (self.eo.player.name, self.so.target_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)


class DefensiveRunOrderTest(RunOrdersTest):
	def test_offensive_protection_offensive(self):
		"""
		Test that the Protection only cancels one Offensive run
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.SABOTAGE
		)
		po.clean()
		po.save()

		begin_assets = self.so.target_corporation.assets

		po.additional_percents = 10
		po.save()
		self.so.additional_percents = 10
		self.so.save()

		# Should be intercepted
		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)