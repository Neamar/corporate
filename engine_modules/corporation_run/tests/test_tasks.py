from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import ProtectionOrder, SabotageOrder


class OffensiveRunTaskTest(EngineTestCase):
	def setUp(self):

		super(OffensiveRunTaskTest, self).setUp()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation=self.c,
			additional_percents=0,
		)
		self.so.clean()
		self.so.save()

		# Refill money for the player
		self.INITIAL_MONEY = 100000
		self.p.money = self.INITIAL_MONEY
		self.p.save()

		self.so_initial_extraction = self.so.target_corporation.base_corporation.sabotage

	def test_offensive_run_task(self):
		"""
		Check the task solves the run
		"""
		begin_sabotaged_assets = self.so.target_corporation.assets
		self.so.target_corporation.base_corporation.sabotage = 0
		self.so.additional_percents = 10
		self.so.save()

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_sabotaged_assets - 2)

		self.so.target_corporation.base_corporation.sabotage = self.so_initial_extraction

	def test_protection_run_task(self):
		"""
		Check the task solves the run
		"""
		po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.SABOTAGE,
		)
		po.clean()
		po.save()
		po.additional_percents = 10
		po.save()

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).money, self.INITIAL_MONEY - po.get_cost())
