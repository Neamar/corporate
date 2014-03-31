from engine.testcases import EngineTestCase
from engine_modules.derivative.models import Derivative


class OrdersTest(EngineTestCase):
	def setUp(self):

		super(OrdersTest, self).setUp()

		self.d = Derivative(name="derivative", game=self.g)
		self.d.save()
		self.d.corporations.add(self.c, self.c2)

	def test_derivative_get_sum(self):
		"""
		Should return assets
		"""
		initial_assets = self.c.assets

		self.c.assets = 25
		self.c.save()
		self.g.resolve_current_turn()

		old_value = self.d.get_sum(self.g.current_turn - 2)
		self.assertEqual(old_value, initial_assets + self.c2.assets)

		current_value = self.d.get_sum(self.g.current_turn - 1)
		self.assertEqual(current_value, self.c.assets + self.c2.assets)
