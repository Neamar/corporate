from engine_modules.corporation_run.tests.test_orders import RunOrdersTest
from engine.models import Player
from engine_modules.player_run.models import InformationOrder


class InformationRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(InformationRunOrderTest, self).setUp()

		self.p2 = Player(game=self.g, secrets="Some nasty sfuff")
		self.p2.save()
		citizenship = self.p2.citizenship
		citizenship.corporation = self.c
		citizenship.save()

		from engine_modules.influence.models import BuyInfluenceOrder

		# Initial setup, create logs we'll use later.
		o = BuyInfluenceOrder(
			player=self.p2
		)
		o.save()

		self.g.resolve_current_turn()

		self.io = InformationOrder(
			target=self.p2,
			player=self.p,
			additional_percents=0,
		)
		self.io.clean()
		self.io.save()

		self.set_to_zero(self.io.target.citizenship.corporation)

	def tearDown(self):
		self.set_to_original(self.io.target.citizenship.corporation)
