# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder, datasteal_messages, sabotage_messages

DEBUG = False

class RunOrdersTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless")
		self.bc.save()
		self.bc2 = BaseCorporation(name="Renraku", description="Priceless")
		self.bc2.save()
		self.bc3 = BaseCorporation(name="Ares", description="Ruthless")
		self.bc3.save()

		super(RunOrdersTest, self).setUp()

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

		self.p.money = 100000
		self.p.save()


class OffensiveRunOrderTest(RunOrdersTest):
	def test_datasteal_success(self):
		"""
		Datasteal benefits the stealer 1 asset without costing the stolen
		"""	
		
		if DEBUG : print "-"*90+"\n\ttest_datasteal_success"
		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets
		self.dso.additional_percents = 10
		self.dso.save()

		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)		

		note = self.dso.player.note_set.get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['success'].format(self.dso.target_corporation.base_corporation.name, self.dso.stealer_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_datasteal_failure(self):
		"""
		Dailed datasteal should not change corporation assets.
		"""

		if DEBUG : print "-"*90+"\n\ttest_datasteal_failure"
		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)		

		note = self.dso.player.note_set.get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['fail'].format(self.dso.target_corporation.base_corporation.name, self.dso.stealer_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_datasteal_interception(self):
		"""
		Intercepted datasteal should not change corporation assets.
		"""

		if DEBUG : print "-"*90+"\n\ttest_datasteal_interception"
		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.po.additional_percents = 10
		self.po.save()
		self.dso.additional_percents = 10
		self.dso.resolve()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)		
		
		aggressor_note = self.dso.player.note_set.get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['interception']['aggressor'].format(self.dso.target_corporation.base_corporation.name, self.dso.stealer_corporation.base_corporation.name)
		self.assertEqual(aggressor_note.content, expected_message)

		protector_note = self.po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = datasteal_messages['interception']['protector'].format(self.dso.target_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)

	def test_datasteal_capture(self):
		"""
		Captured datasteal should not change corporation assets.
		"""

		if DEBUG : print "-"*90+"\n\ttest_datasteal_capture"
		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.po.additional_percents = 10
		self.po.save()
		self.dso.additional_percents = 0
		self.dso.resolve()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)		
		
		aggressor_note = self.dso.player.note_set.get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['capture']['aggressor'].format(self.dso.target_corporation.base_corporation.name)
		self.assertTrue(aggressor_note.content, expected_message)

		protector_note = self.po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = datasteal_messages['capture']['protector'].format(self.dso.player.name, self.dso.target_corporation.base_corporation.name, self.dso.stealer_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)

	def test_multiple_datasteal(self):
		"""
		Only the first successful DataSteal on a same corporation can benefit someone.
		The others succeeds, but the clients do not profit from them
		"""

		if DEBUG : print "-"*90+"\n\ttest_multipledatasteal"

		dso2 = DataStealOrder(
			stealer_corporation=self.c3,
			player=self.p,
			target_corporation=self.c
		)
		dso2.save()


		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.dso.additional_percents = 10
		self.dso.resolve()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)
		note = self.dso.player.note_set.get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['success'].format(self.dso.target_corporation.base_corporation.name, self.dso.stealer_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

		# Resolve (and fail) second datasteal
		dso2.additional_percents = 10
		dso2.resolve()
		
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)
	
		note = self.dso.player.note_set.exclude(pk=note.pk).get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['late'].format(dso2.target_corporation.base_corporation.name, dso2.stealer_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_sabotage_success(self):
		"""
		Sabotage doesn't benefit anyone, but costs the sabotaged 2 assets
		"""

		if DEBUG : print "-"*90+"\n\ttest_sabotage_success"
		begin_assets = self.so.target_corporation.assets

		self.so.additional_percents = 10
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets - 2)

		note = self.so.player.note_set.get(category=u"Run de Sabotage", turn=self.g.current_turn)
		expected_message = sabotage_messages['success'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_sabotage_failure(self):
		"""
		Failed sabotage does not change corporation assets
		"""

		if DEBUG : print "-"*90+"\n\ttest_sabotage_failure"
		begin_assets = self.so.target_corporation.assets

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

		note = self.so.player.note_set.get(category=u"Run de Sabotage", turn=self.g.current_turn)
		expected_message = sabotage_messages['fail'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_sabotage_interception(self):
		"""
		Intercepted sabotage does not change corporation assets
		"""

		if DEBUG : print "-"*90+"\n\ttest_sabotage_interception"
		begin_assets = self.dso.target_corporation.assets

		self.po.additional_percents = 10
		self.po.save()
		self.so.additional_percents = 10

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)		
		
		aggressor_note = self.so.player.note_set.get(category=u"Run de Sabotage", turn=self.g.current_turn)
		expected_message = sabotage_messages['interception']['aggressor'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(aggressor_note.content, expected_message)

		protector_note = self.po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = sabotage_messages['interception']['protector'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)

	def test_sabotage_capture(self):
		"""
		Captured sabotage does not change corporation assets
		"""

		if DEBUG : print "-"*90+"\n\ttest_sabotage_capture"
		begin_assets = self.so.target_corporation.assets

		self.po.additional_percents = 10
		self.po.save()
		self.so.additional_percents = 0
		self.so.save()

		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)		
		aggressor_note = self.so.player.note_set.get(category=u"Run de Sabotage", turn=self.g.current_turn)
		expected_message = sabotage_messages['capture']['aggressor'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(aggressor_note.content, expected_message)

		protector_note = self.po.player.note_set.get(category=u"Run de Protection", turn=self.g.current_turn)
		expected_message = sabotage_messages['capture']['protector'].format(self.so.player.name, self.so.target_corporation.base_corporation.name)
		self.assertEqual(protector_note.content, expected_message)


class DefensiveRunOrderTest(RunOrdersTest):
	def test_offensive_protection_offensive(self):
		"""
		Test that the Protection only cancels one Offensive run
		"""
		if DEBUG : print "-"*90+"\n\ttest_so_po_so"

		begin_assets = self.so.target_corporation.assets

		self.po.additional_percents = 10
		self.po.save()
		self.so.additional_percents = 10
		self.so.save()

		# Should be intercepted
		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

		# Should not be intercepted
		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets - 2)

	def test_protection_descending_probability(self):
		"""
		Test that Protection Runs are resolved from highest to lowest success probability
		In this case, for testing purposes, the Protection Run with 200 should be
		the one that succeeds, not the one with 100
		"""

		if DEBUG : print "-"*90+"\n\ttest_protection_descending_probability"


		po2 = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			additional_percents=20
		)
		po2.save()

		self.po.additional_percents = 10
		self.po.save()
		self.dso.additional_percents=10
		self.dso.save()
		self.dso.resolve()

		self.assertEqual(self.reload(self.po).done, False)
		self.assertEqual(self.reload(po2).done, True)

