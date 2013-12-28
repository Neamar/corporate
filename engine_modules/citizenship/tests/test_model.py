from django.db import IntegrityError
from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation
from engine_modules.citizenship.orders import CitizenShipOrder


class ModelTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless.")
		self.bc.save()

		self.bc2 = BaseCorporation(name="AZER", description="TY")
		self.bc2.save()

		super(ModelTest, self).setUp()

		self.c = Corporation.objects.get(base_corporation=self.bc)
		self.c.assets = 10
		self.c.save()

		self.c2 = Corporation.objects.get(base_corporation=self.bc2)
		self.c2.assets = 15
		self.c2.save()

	def test_player_cant_have_two_cities(self):
		"""
		The player can't have twocitizenships
		"""
		o = CitizenShipOrder(corporation=self.c, player=self.p)
		o.save()

		o.resolve()

		o2 = CitizenShipOrder(corporation=self.c2, player=self.p)
		o2.save()

		self.assertRaises(IntegrityError, o2.resolve())