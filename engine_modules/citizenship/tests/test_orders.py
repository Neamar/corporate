from engine.testcases import EngineTestCase
from engine_modules.citizenship.models import CitizenShipOrder


class OrdersTest(EngineTestCase):
	def setUp(self):
		super(OrdersTest, self).setUp()

		self.o = CitizenShipOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.clean()
		self.o.save()

	def test_citizenship_is_affected(self):
		"""
		Check if the citizenship is created
		"""
		self.o.resolve()

		self.assertEqual(self.reload(self.p).citizenship.corporation, self.c)
