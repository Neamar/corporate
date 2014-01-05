from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder
from engine.exceptions import OrderNotAvailable
from engine_modules.vote.tests.test_orders import OrdersTest
from engine_modules.corporation.models import BaseCorporation, Corporation

class RunOrdersTest(OrdersTest):
	def setUp(self):
		super(RunOrdersTest, self).setUp()

		self.c.protected = None
		self.c.save()
		
		self.c2.protected = None
		self.c2.save()

		self.dso = DataStealOrder(
			player=self.p,
			stealer_corporation=self.c2,
			stolen_corporation=self.c
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
			sabotaged_corporation = self.c
		)
		self.so.clean()
		self.so.save()

	def test_datasteal_success(self):
		"""
		Datasteal benefits the stealer 1 asset without costing the stolen
		"""

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.stolen_corporation.assets

		self.dso.resolve_successful()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
		self.assertEqual(self.reload(self.dso.stolen_corporation).assets, begin_assets_stolen)		

	def test_datasteal_failure(self):

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.stolen_corporation.assets

		self.dso.resolve_failure()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso.stolen_corporation).assets, begin_assets_stolen)		

	def test_sabotage_successful(self):
		"""
		Sabotage doesn't benefit anyone, but costs the sabotaged 2 assets
		"""

		begin_assets = self.so.sabotaged_corporation.assets

		self.so.resolve_successful()

		self.assertEqual(self.reload(self.so.sabotaged_corporation).assets, begin_assets - 2)

	def test_sabotage_failure(self):

		begin_assets = self.so.sabotaged_corporation.assets

		self.so.resolve_failure()
		self.assertEqual(self.reload(self.so.sabotaged_corporation).assets, begin_assets)

	def test_multiple_datasteal(self):
		"""
		Only the first successful DataSteal on a same corporation can benefit someone
		The others succeed, but the clients do not profit from them
		"""

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.stolen_corporation.assets

		self.dso.resolve_successful()
		self.dso.clean()

		self.dso.resolve_successful()	
		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer + 1)
	
	def test_so_po(self):
		"""
		Test that the Protection cancels the Sabotage
		"""

		begin_assets = self.so.sabotaged_corporation.assets
		truc = self.so.sabotaged_corporation.protecteurs.all()
		print "Truc: "
		print truc

		self.po.resolve_successful()
		self.so.resolve_successful()
		self.assertEqual(self.reload(self.so.sabotaged_corporation).assets, begin_assets)

	def test_so_po_so(self):
		"""
		Test that the Protection only cancels one Sabotage
		"""

		begin_assets = self.so.sabotaged_corporation.assets

		self.po.resolve_successful()
		self.so.resolve_successful()
		self.so.clean()
		self.so.resolve_successful()
		self.assertEqual(self.reload(self.so.sabotaged_corporation).assets, begin_assets - 2)

	def test_dso_po_dso_dso(self):
		"""
		In that case, the first DataSteal fails because of the Protection, so the second
		should succeed and benefit the client while the third succeeds without benefits
		"""

		self.bc3 = BaseCorporation(name="Hero", description="Kaamoulox")
		self.bc3.save()
		
		self.c3 = Corporation(game=self.g, base_corporation=self.bc3)
		self.c3.assets = 20
		self.c3.protected = False
		self.c3.save()

		self.dso2 = DataStealOrder(
			player=self.p,
			stealer_corporation=self.c3,
			stolen_corporation=self.c
		)
		self.dso2.save()

		begin_assets_stealer1 = self.dso.stealer_corporation.assets
		begin_assets_stealer2 = self.dso2.stealer_corporation.assets
		begin_assets_stolen = self.dso.stolen_corporation.assets

		self.po.resolve_successful()
		self.dso.resolve_successful() #it says successful, but the protection is here
		self.dso2.resolve_successful()
		self.dso.clean()
		self.dso.resolve_successful()

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_assets_stealer1)
		self.assertEqual(self.reload(self.dso2.stealer_corporation).assets, begin_assets_stealer2 + 1)
