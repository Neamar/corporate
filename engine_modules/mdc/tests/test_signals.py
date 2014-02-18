from engine.testcases import EngineTestCase
from engine_modules.mdc.models import MDCVoteOrder
from engine.exceptions import OrderNotAvailable


class SignalsTest(EngineTestCase):
	def setUp(self):
		super(SignalsTest, self).setUp()

	def test_one_vote(self):
		"""
		Can't vote more than once
		"""
		v = MDCVoteOrder(
			player=self.p,
		)
		v.clean()
		v.save()

		v2 = MDCVoteOrder(
			player=self.p,
		)
		self.assertRaises(OrderNotAvailable, v2.clean)
