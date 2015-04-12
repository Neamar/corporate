from engine.testcases import EngineTestCase
from engine_modules.detroit_inc.models import DIncVoteOrder
from engine.exceptions import OrderNotAvailable


class SignalsTest(EngineTestCase):
	def setUp(self):
		super(SignalsTest, self).setUp()

	def test_one_vote(self):
		"""
		Can't vote more than once
		"""
		v = DIncVoteOrder(
			player=self.p,
		)
		v.clean()
		v.save()

		v2 = DIncVoteOrder(
			player=self.p,
		)
		self.assertRaises(OrderNotAvailable, v2.clean)
