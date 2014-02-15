from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder


class OffensiveRunTaskTest(EngineTestCase):
	def setUp(self):

		super(OffensiveRunTaskTest, self).setUp()

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

		self.po = ProtectionOrder(
			player=self.p,
			protected_corporation=self.c,
			defense=ProtectionOrder.SABOTAGE
		)
		self.po.clean()
		self.po.save()

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

	def test_offensive_run_task(self):
		"""
		Check the task solves the run
		"""
		begin_sabotaged_assets = self.so.target_corporation.assets

		self.so.additional_percents = 10
		self.so.save()

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.so.target_corporation).assets, begin_sabotaged_assets - 2)

	def test_protection_run_task(self):
		"""
		Check the task solves the run
		"""
		self.po.additional_percents = 10
		self.po.save()

		self.g.resolve_current_turn()
		self.assertEqual(self.p.money, self.INITIAL_MONEY - self.po.get_cost())