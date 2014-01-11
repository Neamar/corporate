# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation
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

		self.c = Corporation.objects.get(base_corporation=self.bc)
		self.c.assets = 10
		self.c.save()

		self.c2 = Corporation.objects.get(base_corporation=self.bc2)
		self.c2.assets = 15
		self.c2.save()

		self.c3 = Corporation.objects.get(base_corporation=self.bc3)
		self.c3.assets = 20
		self.c3.save()

		self.dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c
		)
		self.dso.clean()
		self.dso.save()

		self.dso2 = DataStealOrder(
			stealer_corporation=self.c3,
			player=self.p,
			target_corporation=self.c
		)
		self.dso2.save()

		self.po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c
		)
		self.po.clean()
		self.po.save()

		self.po2 = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c
		)
		self.po2.clean()
		self.po2.save()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation = self.c
		)
		self.so.clean()
		self.so.save()

		self.p.money = 100000
		self.p.save()

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
		self.dso2.additional_percents = 10
		self.dso2.resolve()
		
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)
	
		note = self.dso.player.note_set.exclude(pk=note.pk).get(category=u"Run de Datasteal", turn=self.g.current_turn)
		expected_message = datasteal_messages['late'].format(self.dso2.target_corporation.base_corporation.name, self.dso2.stealer_corporation.base_corporation.name)
		self.assertEqual(note.content, expected_message)

	def test_sabotage_success(self):
		"""
		Sabotage doesn't benefit anyone, but costs the sabotaged 2 assets
		"""

		if DEBUG : print "-"*90+"\n\ttest_sabotage_success"
		begin_assets = self.so.target_corporation.assets

		self.so.additional_percents=10
		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets - 2)

		notes = self.so.player.note_set.filter(category=u"Run de Sabotage", turn=self.g.current_turn)
		self.assertEqual(len(notes), 1)
		expected_message = sabotage_messages['success'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(notes[0].content, expected_message)

	def test_sabotage_failure(self):

		if DEBUG : print "-"*90+"\n\ttest_sabotage_failure"
		begin_assets = self.so.target_corporation.assets

		self.assertEqual(self.so.get_success_probability(), 0)
		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

		notes = self.so.player.note_set.filter(category=u"Run de Sabotage", turn=self.g.current_turn)
		self.assertEqual(len(notes), 1)
		expected_message = sabotage_messages['fail'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(notes[0].content, expected_message)

	def test_sabotage_interception(self):
		
		if DEBUG : print "-"*90+"\n\ttest_sabotage_interception"
		begin_assets = self.dso.target_corporation.assets

		self.po.additional_percents=10
		self.po.save()
		self.assertEqual(self.po.get_success_probability(), 100)
		self.so.additional_percents=10
		self.so.resolve()

		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)		
		
		aggressor_notes = self.so.player.note_set.filter(category=u"Run de Sabotage", turn=self.g.current_turn)
		self.assertEqual(len(aggressor_notes), 1)
		expected_message = sabotage_messages['interception']['aggressor'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(aggressor_notes[0].content, expected_message)

		protector_notes = self.po.player.note_set.filter(category=u"Run de Protection", turn=self.g.current_turn)
		self.assertEqual(len(protector_notes), 1)
		expected_message = sabotage_messages['interception']['protector'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(protector_notes[0].content, expected_message)

	def test_sabotage_capture(self):
		
		if DEBUG : print "-"*90+"\n\ttest_sabotage_capture"
		begin_assets = self.so.target_corporation.assets

		self.po.additional_percents=10
		self.po.save()
		self.assertEqual(self.po.get_success_probability(), 100)
		self.so.additional_percents=00
		self.so.save()
		self.assertEqual(self.so.get_success_probability(), 0)
		self.so.resolve()

		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)		
		aggressor_notes = self.so.player.note_set.filter(category=u"Run de Sabotage", turn=self.g.current_turn)
		self.assertEqual(len(aggressor_notes), 1)
		expected_message = sabotage_messages['capture']['aggressor'].format(self.so.target_corporation.base_corporation.name)
		self.assertEqual(aggressor_notes[0].content, expected_message)

		protector_notes = self.reload(self.po.player).note_set.filter(category=u"Run de Protection", turn=self.g.current_turn)
		self.assertEqual(len(protector_notes), 1)
		expected_message = sabotage_messages['capture']['protector'].format(self.so.player.name, self.so.target_corporation.base_corporation.name)
		self.assertEqual(protector_notes[0].content, expected_message)

	def test_so_po(self):
		"""
		Test that the Protection cancels the Sabotage
		"""

		if DEBUG : print "-"*90+"\n\ttest_so_po"
		begin_assets = self.so.target_corporation.assets

		self.po.additional_percents=10
		self.po.save()
		self.assertEqual(self.po.get_success_probability(), 100)
		self.so.additional_percents=10
		self.so.save()
		self.assertEqual(self.so.get_success_probability(), 100)
		self.assertEqual(self.po.get_success_probability(), 100)
		self.so.resolve()

		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

	def test_so_po_so(self):
		"""
		Test that the Protection only cancels one Sabotage
		"""
		if DEBUG : print "-"*90+"\n\ttest_so_po_so"

		begin_assets = self.so.target_corporation.assets

		self.po.additional_percents=10
		self.po.save()
		self.assertEqual(self.po.get_success_probability(), 100)
		self.so.additional_percents=10
		self.so.save()
		self.assertEqual(self.so.get_success_probability(), 100)
		self.so.resolve()
		self.so.clean()
		self.so.additional_percents=10
		self.so.save()
		self.assertEqual(self.so.get_success_probability(), 100)
		self.so.resolve()
		self.so.clean()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets - 2)

	def test_dso_po_dso_dso(self):
		"""
		In that case, the first DataSteal fails because of the Protection, so the second
		should succeed and benefit the client while the third succeeds without benefits
		"""

		if DEBUG : print "-"*90+"\n\ttest_dso_po_dso_dso"
		begin_assets_stealer1 = self.dso.stealer_corporation.assets
		begin_assets_stealer2 = self.dso2.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.po.additional_percents=10
		self.po.save()
		self.assertEqual(self.po.get_success_probability(), 100)
		self.dso.additional_percents=10
		self.dso.save()
		self.assertEqual(self.dso.get_success_probability(), 100)
		self.dso.resolve()
		self.dso2.additional_percents=10
		self.dso2.save()
		self.assertEqual(self.dso2.get_success_probability(), 100)
		self.dso2.resolve()
		self.dso.clean()
		self.dso.additional_percents=10
		self.dso.save()
		self.assertEqual(self.dso.get_success_probability(), 100)
		self.dso.resolve()

		# This test was failing because the multiple dso limit was not yet implemented
		# The line beneath tests two aspects, if it fails, test_multiple datasteals should too
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer1)
		self.assertEqual(self.reload(self.dso2.stealer_corporation).assets, begin_assets_stealer2 + 1)

	def test_protection_fail_success(self):
		"""
		In that case, the Protection fails on the first Offensive Run, but succeeds on the second
		The first Offensive Run should therefore succeed while the second should fail
		"""

		if DEBUG : print "-"*90+"\n\ttest_protection_fail_success"
		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_sabotaged = self.so.target_corporation.assets

		self.assertEqual(self.po.get_success_probability(), 0)
		self.dso.additional_percents=10
		self.dso.save()
		self.assertEqual(self.dso.get_success_probability(), 100)
		self.dso.resolve()
		self.po.additional_percents=10
		self.assertEqual(self.po.get_success_probability(), 100)
		self.po.save()
		self.assertEqual(self.po.get_success_probability(), 100)
		self.so.additional_percents=10
		self.so.save()
		self.assertEqual(self.so.get_success_probability(), 100)
		self.so.resolve()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets_sabotaged)

	def test_protection_descending_probability(self):
		"""
		Test that Protection Runs are resolved from highest to lowest success probability
		In this case, for testing purposes, the Protection Run with 200 should be
		the one that succeeds, not the one with 100
		"""

		if DEBUG : print "-"*90+"\n\ttest_protection_descending_probability"
		self.po.additional_percents=10
		self.po.save()
		self.assertEqual(self.po.get_success_probability(), 100)
		self.po2.additional_percents=20
		self.po2.save()
		self.assertEqual(self.po2.get_success_probability(), 200)
		self.dso.additional_percents=10
		self.dso.save()
		self.assertEqual(self.dso.get_success_probability(), 100)
		self.dso.resolve()

		self.assertEqual(self.reload(self.po).done, False)
		self.assertEqual(self.reload(self.po2).done, True)

