from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation
from engine_modules.speculation.models import SpeculationOrder
from engine.exceptions import OrderNotAvailable


class SignalsTest(EngineTestCase):
	def setUp(self):
		super(SignalsTest, self).setUp()

		self.g.corporation_set.all().delete()

		self.first_corporation = Corporation(base_corporation_slug='Last', assets=100)
		self.g.corporation_set.add(self.first_corporation)
		self.medium_corporation = Corporation(base_corporation_slug='Medium', assets=10)
		self.g.corporation_set.add(self.medium_corporation)
		self.last_corporation = Corporation(base_corporation_slug='First', assets=1)
		self.g.corporation_set.add(self.last_corporation)

	def test_max_speculation(self):
		self.p.influence.level = 1

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

		self.p.influence.level = 2
		self.p.influence.save()

		# assertNoRaises
		o2.clean()

	def test_max_speculation_amount(self):
		self.p.influence.level = 1;

		o = SpeculationOrder(
			player=self.p,
			corporation=self.last_corporation,
			rank=1,
			investment=51
		)
		self.assertRaises(OrderNotAvailable, o.clean)