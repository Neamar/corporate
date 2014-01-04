from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder
from engine.exceptions import OrderNotAvailable
from engine_modules.vote.tests.test_orders import OrdersTest

class RunOrdersTest(OrdersTest):
	def setUp(self):
		super(RunOrdersTest, self).setUp()
		
		self.dso = DataStealOrder(
			player=self.p,
			stealer_corporation=self.c,
			stolen_corporation=self.c2
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
	"""
	Datasteal benefits the stealer 1 asset without costing the stolen
	"""
	def test_datasteal_success(self):

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.stolen_corporation.assets

		self.dso.resolve_successful()

		self.assertEqual(self.reload(self.dso).stealer_corporation.assets, begin_assets_stealer + 1)
		self.assertEqual(self.reload(self.dso).stolen_corporation.assets, begin_assets_stolen)		
	def test_datasteal_failure(self):

		begin_assets_stealer = self.dso.stealer_corporation.assets
		begin_assets_stolen = self.dso.stolen_corporation.assets

		self.dso.resolve_failure()

		self.assertEqual(self.reload(self.dso).stealer_corporation.assets, begin_assets_stealer)
		self.assertEqual(self.reload(self.dso).stolen_corporation.assets, begin_assets_stolen)		
	"""
	Sabotage doesn't benefit anyone, but costs the sabotaged 2 assets
	"""
	def test_sabotage_successful(self):

		begin_assets = self.so.sabotaged_corporation.assets

		self.so.resolve_successful()

		self.assertEqual(self.reload(self.so).sabotaged_corporation.assets, begin_assets - 2)

	def test_sabotage_failure(self):

		begin_assets = self.so.sabotaged_corporation.assets

		self.so.resolve_failure()
		self.assertEqual(self.reload(self.so).sabotaged_corporation.assets, begin_assets)
