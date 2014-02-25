from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine_modules.citizenship.models import CitizenShipOrder


class SignalsTest(EngineTestCase):
	def setUp(self):

		super(SignalsTest, self).setUp()

		self.o = CitizenShipOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.clean()
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
