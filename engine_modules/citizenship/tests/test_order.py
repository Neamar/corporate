from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine_modules.citizenship.models import CitizenShipOrder
from engine_modules.corporation.models import BaseCorporation


class OrdersTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation("ares")
		self.bc.save()

		super(OrdersTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation=self.bc)

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
		
	def test_cant_create_order_twice(self):
		"""
		Order can't be created twice
		"""	
		o2 = CitizenShipOrder(
			player=self.p,
			corporation=self.c
		)

		self.assertRaises(ValidationError, o2.clean)
