from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder
from engine.exceptions import OrderNotAvailable
from engine_modules.corporation.models import BaseCorporation, Corporation

class RunOrdersTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC", description="Reckless.")
		self.bc.save()

		self.bc2 = BaseCorporation(name="AZ", description="TY")
		self.bc2.save()

		self.bc3 = BaseCorporation(name="Hero", description="Kaamoulox")
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

		self.so = SabotageOrder(
			player=self.p,
			target_corporation = self.c
		)
		self.so.clean()
		self.so.save()

		self.p.money = 100000

	def test_datasteal_success(self):
		"""
		Datasteal benefits the stealer 1 asset without costing the stolen
		"""

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.dso.additional_percents=10
		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)		

	def test_datasteal_failure(self):

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.assertEqual(self.dso.get_success_probability(), 0)
		self.dso.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.target_corporation).assets, begin_assets_stolen)		

	def test_sabotage_success(self):
		"""
		Sabotage doesn't benefit anyone, but costs the sabotaged 2 assets
		"""

		begin_assets = self.so.target_corporation.assets

		self.so.additional_percents=10
		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets - 2)

	def test_sabotage_failure(self):

		begin_assets = self.so.target_corporation.assets

		self.assertEqual(self.so.get_success_probability(), 0)
		self.so.resolve()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets)

	def test_multiple_datasteal(self):
		"""
		Only the first successful DataSteal on a same corporation can benefit someone
		The others succeed, but the clients do not profit from them
		"""
		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.dso.additional_percents=10
		self.dso.resolve()

		self.dso2.additional_percents=10
		self.dso2.resolve()
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
	
	def test_so_po(self):
		"""
		Test that the Protection cancels the Sabotage
		"""

		begin_assets = self.so.target_corporation.assets

		self.po.additional_percents=10
		self.po.save()
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

		begin_assets = self.so.target_corporation.assets

		self.po.additional_percents=10
		self.po.save()
		self.so.additional_percents=10
		self.so.resolve()
		self.so.clean()
		self.so.additional_percents=10
		self.so.resolve()
		self.so.clean()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_assets - 2)

	def test_dso_po_dso_dso(self):
		"""
		In that case, the first DataSteal fails because of the Protection, so the second
		should succeed and benefit the client while the third succeeds without benefits
		"""

		begin_assets_stealer1 = self.dso.stealer_corporation.assets
		begin_assets_stealer2 = self.dso2.stealer_corporation.assets
		begin_assets_stolen = self.dso.target_corporation.assets

		self.po.additional_percents=10
		self.po.save()
		self.dso.additional_percents=10
		self.dso.resolve()
		self.dso2.additional_percents=10
		self.dso2.resolve()
		self.dso.clean()
		self.dso.additional_percents=10
		self.dso.resolve()

		# This test was failing because the multiple dso limit was not yet implemented
		# The line beneath tests two aspects, if it fails, test_multiple datasteals should too
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer1)
		self.assertEqual(self.reload(self.dso2.stealer_corporation).assets, begin_assets_stealer2 + 1)
