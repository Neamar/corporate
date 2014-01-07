from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder
from engine.exceptions import OrderNotAvailable
from engine_modules.corporation.models import BaseCorporation, Corporation
from engine_modules.corporation_run.tasks import OffensiveRunTask

class OffensiveRunTaskTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC", description="Reckless.")
		self.bc.save()

		self.bc2 = BaseCorporation(name="AZ", description="TY")
		self.bc2.save()

		self.bc3 = BaseCorporation(name="Hero", description="Kaamoulox")
		self.bc3.save()

		super(OffensiveRunTaskTest, self).setUp()

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

		self.t = OffensiveRunTask()

	def test_offensive_runs_descending_probability(self):
		"""
		Test that Offensive Runs are resolved from highest to lowest success probability
		In this case, the Datasteal with 200 should be the one that fails (because of 
		the Protection) and the Sabotage with 100 should succeed
		"""

		begin_stealer_assets = self.dso.stealer_corporation.assets
		begin_sabotaged_assets = self.so.target_corporation.assets

		self.po.additional_percents=10
		self.po.save()
		self.dso.additional_percents=20
		self.dso.save()
		self.so.additional_percents=10

		self.assertEqual(self.dso2.get_success_probability(), 0)
		self.assertEqual(self.po2.get_success_probability(), 0)
		self.t.run(self.g)

		self.assertEqual(self.reload(self.dso.stealer_corporation).assets, begin_stealer_assets)
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_sabotaged_assets)
