from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation
from engine_modules.citizenship.orders import CitizenShipOrder


class ModelTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless.")
		self.bc.save()

		super(ModelTest, self).setUp()

		self.c = Corporation.objects.get(base_corporation=self.bc)
		self.c.assets = 10
		self.c.save()

	def test_citizenship_in_affected(self):
		"""
		Check is the citizenship is created
		"""
		o = CitizenShipOrder(corporation=self.c, player=self.p)
		o.save()

		o.resolve()

		self.assertEqual(self.p.citizenship.corporation, self.c)