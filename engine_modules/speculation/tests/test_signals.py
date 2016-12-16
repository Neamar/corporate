from engine.testcases import EngineTestCase
from engine_modules.speculation.models import CorporationSpeculationOrder
from engine.exceptions import OrderNotAvailable


class SignalsTest(EngineTestCase):
	def setUp(self):
		super(SignalsTest, self).setUp()

	def test_max_corporation_speculation_amount_in_single_instance(self):
		"""
		Can't speculate more than influence * MAX_AMOUNT_SPECULATION
		"""
		o = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.c2,
			rank=1,
			investment=self.p.influence.level * CorporationSpeculationOrder.MAX_AMOUNT_SPECULATION + 1
		)
		self.assertRaises(OrderNotAvailable, o.clean)

		influence = self.p.influence
		influence.level = 2
		influence.save()

		# assertNoRaises
		o.clean()

	def test_max_corporation_speculation_amount_in_multiple_instance(self):
		"""
		Can't speculate more than influence * MAX_AMOUNT_SPECULATION, even with many speculations
		"""
		o = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.c2,
			rank=1,
			investment=self.p.influence.level * CorporationSpeculationOrder.MAX_AMOUNT_SPECULATION / 2 + 1
		)
		# assertNoRaises
		o.clean()
		o.save()

		o2 = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.c2,
			rank=1,
			investment=self.p.influence.level * CorporationSpeculationOrder.MAX_AMOUNT_SPECULATION / 2
		)
		self.assertRaises(OrderNotAvailable, o2.clean)
