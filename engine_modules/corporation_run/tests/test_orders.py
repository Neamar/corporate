from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder
from engine.exceptions import OrderNotAvailable
from engine_modules.vote.tests.test_orders import OrdersTest

class RunOrdersTest(OrdersTest):
	def setUp(self):
		super(RunOrdersTest, self).setUp()
		
		self.DSO = DataStealOrder(
			player=self.p,
			stealer_corporation=self.c,
			stolen_corporation=self.c2
		)
		self.DSO.clean()
		self.DSO.save()

		self.PO = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c
		)
		self.PO.clean()
		self.PO.save()

		self.SO = SabotageOrder(
			player=self.p,
			sabotaged_corporation = self.c
		)
		self.SO.clean()
		self.SO.save()

	# Datasteal benefits the stealer 1 asset without costing the stolen
	def test_DataSteal_successful(self):

		begin_assets_stealer = self.DSO.stealer_corporation.assets
		begin_assets_stolen = self.DSO.stolen_corporation.assets

		self.DSO.resolve_successful()

		self.assertEqual(self.DSO.stealer_corporation.assets, begin_assets_stealer + 1)
		self.assertEqual(self.DSO.stolen_corporation.assets, begin_assets_stolen)		
		self.DSO.clean()

	def test_DataSteal_failure(self):

		begin_assets_stealer = self.DSO.stealer_corporation.assets
		begin_assets_stolen = self.DSO.stolen_corporation.assets

		self.DSO.resolve_failure()

		self.assertEqual(self.DSO.stealer_corporation.assets, begin_assets_stealer)
		self.assertEqual(self.DSO.stolen_corporation.assets, begin_assets_stolen)		
		self.DSO.clean()

	# Sabotage doesn't benefit anyone, but costs the sabotaged 2 assets
	def test_Sabotage_successful(self):

		begin_assets = self.SO.sabotaged_corporation.assets

		self.SO.resolve_successful()

		self.assertEqual(self.SO.sabotaged_corporation.assets, begin_assets - 2)
		self.SO.clean()

	def test_Sabotage_failure(self):

		begin_assets = self.SO.sabotaged_corporation.assets

		self.SO.resolve_failure()
		self.assertEqual(self.SO.sabotaged_corporation.assets, begin_assets)
		self.SO.clean()
