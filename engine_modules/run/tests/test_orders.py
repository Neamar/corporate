from engine.testcases import EngineTestCase
from engine_modules.run.models import RunOrder
from engine.exceptions import OrderNotAvailable


class OrdersTest(EngineTestCase):
	def setUp(self):
		super(OrdersTest, self).setUp()
		self.o = RunOrder(
			player=self.p,
			additional_percents=0,
		)
		self.o.clean()
		self.o.save()

	def test_resolve_successful_abstract(self):
		self.assertRaises(NotImplementedError, self.o.resolve_successful)

	def test_order_cost_money(self):
		"""
		Money should be reduced
		"""
		def resolve(o):
			"""
			Resolve run o, without NotImplementedError (we don't care about this, that's not waht we want to test)
			"""
			try:
				o.resolve()
			except NotImplementedError:
				pass

		resolve(self.o)
		self.assertEqual(self.reload(self.p).money, self.initial_money)

		self.o.has_influence_bonus = True
		resolve(self.o)
		self.assertEqual(self.reload(self.p).money, self.initial_money)

		self.o.additional_percents = 2
		resolve(self.o)
		self.assertEqual(self.reload(self.p).money, self.initial_money - RunOrder.BASE_COST * 2)

	def test_run_probability(self):
		self.assertEqual(self.o.get_success_probability(), 0)

		self.o.has_influence_bonus = True
		self.assertEqual(self.o.get_success_probability(), 30)

		self.o.additional_percents = 2
		self.assertEqual(self.o.get_success_probability(), 50)

		# We can have 100% probability, but only in test env.
		self.o.additional_percents = 7
		self.assertEqual(self.o.get_success_probability(), 100)

	def test_only_influence_run_has_bonus(self):
		"""
		Influence bonus can only be given to as much run as your current influence level
		"""

		self.o.has_influence_bonus = True
		self.o.save()

		o2 = RunOrder(
			player=self.p,
			has_influence_bonus=True
		)
		self.assertRaises(OrderNotAvailable, o2.clean)

		self.p.influence.level = 2
		self.p.influence.save()

		# assertNoRaises
		o2.clean()

	def test_no_more_than_90(self):
		"""
		User can't have more than 90% chance of success
		"""

		self.o.has_influence_bonus = True
		self.o.additional_percents = 7

		self.assertRaises(OrderNotAvailable, self.o.clean)

		self.o.has_influence_bonus = False
		# assertNoRaises
		self.o.clean()
