from engine.testcases import EngineTestCase
from engine_modules.run.models import RunOrder


class OrdersTest(EngineTestCase):
	def setUp(self):
		super(OrdersTest, self).setUp()
		self.o = RunOrder(
			player=self.p,
			additional_percents=0,
		)
		# Because orders are now given the influence bonus by default, we have to manually take it away
		self.o.clean()
		self.o.has_RSEC_bonus = False
		self.o.save()

	def test_resolve_successful_abstract(self):
		self.assertRaises(NotImplementedError, self.o.resolve_successful)

	def test_order_cost_money(self):
		"""
		Money should be reduced
		"""
		def resolve(o):
			"""
			Resolve run o, without NotImplementedError (we don't care about this, that's not what we want to test)
			"""
			try:
				o.resolve()
			except NotImplementedError:
				pass

		resolve(self.o)

		self.assertEqual(self.reload(self.p).money, self.initial_money - RunOrder.LAUNCH_COST)

		current_player_money = self.reload(self.p).money
		self.o.has_RSEC_bonus = True

		resolve(self.o)

		self.assertEqual(self.reload(self.p).money, current_player_money - RunOrder.LAUNCH_COST + min(RunOrder.INFLUENCE_BONUS, RunOrder.LAUNCH_COST))

		current_player_money = self.reload(self.p).money
		self.o.additional_percents = 2

		resolve(self.o)

		self.assertEqual(self.reload(self.p).money, current_player_money - RunOrder.LAUNCH_COST + min(RunOrder.INFLUENCE_BONUS, RunOrder.LAUNCH_COST + RunOrder.BASE_COST * 2) - RunOrder.BASE_COST * 2)

	def test_run_probability(self):
		self.assertEqual(self.o.get_success_probability(), RunOrder.BASE_SUCCESS_PROBABILITY)

		self.o.has_RSEC_bonus = True
		self.assertEqual(self.o.get_success_probability(), RunOrder.BASE_SUCCESS_PROBABILITY)

		self.o.additional_percents = 2
		self.assertEqual(self.o.get_success_probability(),
				RunOrder.BASE_SUCCESS_PROBABILITY + 2 * 10)

		# We can have 100% probability, but only in test env.
		self.o.additional_percents = 5
		self.assertEqual(self.o.get_success_probability(), 100)
