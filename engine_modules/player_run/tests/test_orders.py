from engine_modules.corporation_run.tests.test_orders import RunOrdersTest
from engine.models import Player
from messaging.models import Message
from engine_modules.player_run.models import InformationOrder


class InformationRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(InformationRunOrderTest, self).setUp()

		self.p2 = Player(game=self.g, secrets="Some nasty sfuff")
		self.p2.save()
		self.p2.citizenship.corporation = self.c
		self.p2.citizenship.save()

		from engine_modules.influence.models import BuyInfluenceOrder

		# Initial setup, create a resolution sheet we'll use later.
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

	def test_information_success(self):
		"""
		Information yields players data
		"""
		self.io.additional_percents = 10
		self.io.save()
		# Save message
		p2_resolution_message = self.p2.message_set.get(flag=Message.RESOLUTION, turn=1).content

		self.g.resolve_current_turn()

		p_results = self.p.message_set.get(flag=Message.PRIVATE_MESSAGE).content

		self.assertIn("Tour 1", p_results)
		self.assertIn(self.p2.secrets, p_results)
		self.assertNotIn("Tour 2", p_results)  # Current turn not included

		self.assertIn(p2_resolution_message, p_results)

	def test_information_failure(self):
		"""
		Failed information should not give information
		"""
		self.io.hidden_percents -= 10
		self.io.save()
		self.g.resolve_current_turn()

		self.assertRaises(Message.DoesNotExist, lambda: self.p.message_set.get(flag=Message.PRIVATE_MESSAGE))
