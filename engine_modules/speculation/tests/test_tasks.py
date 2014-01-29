from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation
from engine_modules.speculation.models import CorporationSpeculationOrder


class TasksTest(EngineTestCase):
	def setUp(self):

		super(TasksTest, self).setUp()
		self.g.corporation_set.all().delete()

		self.first_corporation = Corporation(base_corporation_slug='ares', assets=100)
		self.g.corporation_set.add(self.first_corporation)
		self.medium_corporation = Corporation(base_corporation_slug='renraku', assets=10)
		self.g.corporation_set.add(self.medium_corporation)
		self.last_corporation = Corporation(base_corporation_slug='shiawase', assets=1)
		self.g.corporation_set.add(self.last_corporation)

		self.o = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.first_corporation,
			rank=1,
			investment=5
		)
		self.o.save()

	def test_corporation_speculation(self):
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.p).money, self.initial_money + 100)