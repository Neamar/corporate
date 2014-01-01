from engine.testcases import EngineTestCase
from engine_modules.run.models import RunOrder


class OrdersTest(EngineTestCase):
	def setUp(self):
		super(OrdersTest, self).setUp()
		self.o = RunOrder(
			player=self.p
		)
		self.o.clean()
		self.o.save()

	def test_order_cost_money(self):
		"""
		Money should be reduced
		"""
		def resolve(o):
			"""
			Resolve run o, without NotImplementedError
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

		self.o.additional_percents = 10
		self.assertEqual(self.o.get_success_probability(), 90)
