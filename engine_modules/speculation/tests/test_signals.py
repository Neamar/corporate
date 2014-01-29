from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation
from engine_modules.speculation.models import SpeculationOrder
from engine.exceptions import OrderNotAvailable


class SignalsTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="Last", description="looser", initials_assets=1)
		self.bc.save()
		self.bc2 = BaseCorporation(name="Medium", description="useless", initials_assets=10)
		self.bc2.save()
		self.bc3 = BaseCorporation(name="First", description="Winner", initials_assets=100)
		self.bc3.save()

		super(SignalsTest, self).setUp()

		self.last_corporation = self.g.corporation_set.get(base_corporation=self.bc)
		self.medium_corporation = self.g.corporation_set.get(base_corporation=self.bc2)
		self.first_corporation = self.g.corporation_set.get(base_corporation=self.bc3)

	def test_max_speculation(self):
		self.p.influence.level = 1;

		o = SpeculationOrder(
			player=self.p,
			corporation=self.last_corporation,
			rank=1,
			investment=5
		)
		o.save()

		o2 = SpeculationOrder(
			player=self.p,
			corporation=self.last_corporation,
			rank=1,
			investment=5
		)
		self.assertRaises(OrderNotAvailable, o2.clean)