from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation
from engine_modules.speculation.models import SpeculationOrder


class TasksTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="Last", description="looser", initials_assets=1)
		self.bc.save()
		self.bc2 = BaseCorporation(name="Medium", description="useless", initials_assets=10)
		self.bc2.save()
		self.bc3 = BaseCorporation(name="First", description="Winner", initials_assets=100)
		self.bc3.save()

		super(TasksTest, self).setUp()

		self.last_corporation = self.g.corporation_set.get(base_corporation=self.bc)
		self.medium_corporation = self.g.corporation_set.get(base_corporation=self.bc2)
		self.first_corporation = self.g.corporation_set.get(base_corporation=self.bc3)

		o = SpeculationOrder(
			player=self.p,
			corporation=self.first_corporation,
			rank=1,
			investment=5
		)
		o.save()

	def test_speculation(self):
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.p).money, self.initial_money + 100)