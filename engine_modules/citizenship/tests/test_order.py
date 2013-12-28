from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine_modules.citizenship.orders import CitizenShipOrder
from engine_modules.corporation.models import BaseCorporation, Corporation


class OrdersTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless.")
		self.bc.save()

		super(OrdersTest, self).setUp()

		self.c = Corporation.objects.get(base_corporation=self.bc)
		self.c.assets = 10
		self.c.save()

		self.o = CitizenShipOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.save()

	def test_cant_create_order_twice(self):
		"""
		Order can't be created twice
		"""	
		o2 = CitizenShipOrder(
			player=self.p,
			corporation=self.c
		)

		self.assertRaises(ValidationError, o2.clean)