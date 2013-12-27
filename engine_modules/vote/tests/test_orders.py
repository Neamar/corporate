from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
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

	def test_cant_vote_more_than_influence(self):
		self.p.influence.level=1
		self.p.save()

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
		# assertNoRaises
		o.save()
		

		o2 = VoteOrder(
			corporation_up=c, 
			corporation_down=c2, 
			player=self.p
		)
		
		self.assertRaises(OrderNotAvailable, o2.clean)

		self.p.influence.level=2
		self.p.save()

		# assertNoRaises
		o.clean()