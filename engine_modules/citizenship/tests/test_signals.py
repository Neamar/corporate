from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine_modules.citizenship.models import CitizenShipOrder
from engine_modules.share.models import Share


class SignalsTest(EngineTestCase):
	def setUp(self):

		super(SignalsTest, self).setUp()

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

	def test_cant_create_order_twice(self):
		"""
		Order can't be created twice
		"""
		o2 = CitizenShipOrder(
			player=self.p,
			corporation=self.c
		)

		self.assertRaises(ValidationError, o2.clean)

	def test_cant_get_citizenship_without_share(self):
		"""
		You need at least one share to get citizenship
		"""
		self.s.delete()
		self.o.delete()
		self.assertRaises(ValidationError, self.o.clean)
