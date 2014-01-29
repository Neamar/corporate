from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
from engine_modules.vote.models import VoteOrder


class OrdersTest(EngineTestCase):
	def setUp(self):

		super(OrdersTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation_slug="renraku")
		self.c2 = self.g.corporation_set.get(base_corporation_slug="shiawase")

	def test_corporation_up_and_down(self):
		
		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets
		o = VoteOrder(
			corporation_up=self.c, 
			corporation_down=self.c2, 
			player=self.p
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.c).assets, begin_assets_1 + 1)
		self.assertEqual(self.reload(self.c2).assets, begin_assets_2 - 1)

	def test_cant_vote_more_than_influence(self):
		self.p.influence.level=1
		self.p.save()


		o = VoteOrder(
			corporation_up=self.c, 
			corporation_down=self.c2, 
			player=self.p
		)
		# assertNoRaises
		o.save()
		

		o2 = VoteOrder(
			corporation_up=self.c, 
			corporation_down=self.c2, 
			player=self.p
		)
		
		self.assertRaises(OrderNotAvailable, o2.clean)

		self.p.influence.level=2
		self.p.save()

		# assertNoRaises
		o.clean()
