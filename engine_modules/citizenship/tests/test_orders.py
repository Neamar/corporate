from engine.testcases import EngineTestCase
from engine_modules.citizenship.models import CitizenShipOrder
from engine_modules.share.models import Share


class OrdersTest(EngineTestCase):
	def setUp(self):
		super(OrdersTest, self).setUp()

		self.s = Share(
			player=self.p,
			corporation=self.c
		)
		self.s.save()

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
