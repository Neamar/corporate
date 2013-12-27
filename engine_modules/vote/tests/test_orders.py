from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation
from engine_modules.vote.orders import VoteOrder

class OrdersTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless.")
		self.bc.save()

		self.bc2 = BaseCorporation(name="AZER", description="TY")
		self.bc2.save()

		super(OrdersTest, self).setUp()
		

	def test_corporation_up_and_down(self):
		c = Corporation.objects.get(base_corporation=self.bc)
		c.assets = 10
		c.save()

		c2 = Corporation.objects.get(base_corporation=self.bc2)
		c2.assets = 15
		c2.save()

		o = VoteOrder(
			corporation_up=c, 
			corporation_down=c2, 
			player=self.p
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(c).assets, 11)
		self.assertEqual(self.reload(c2).assets, 14)