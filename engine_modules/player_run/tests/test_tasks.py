from engine.testcases import EngineTestCase
from engine.models import Player
from messaging.models import Message
from engine_modules.player_run.models import InformationRunOrder


class TaskTest(EngineTestCase):
	def test_information_run_success(self):
		"""
		Check we get a message with target player order
		"""
		p2 = Player(game=self.g, money=self.initial_money)
		p2.save()

		# Initial setup, create a resolutoin sheet we'll use later.
		from engine_modules.influence.models import BuyInfluenceOrder
		o = BuyInfluenceOrder(
			player=self.p
		)
		o.save()

		self.g.resolve_current_turn()
		# Save message
		p_m = self.p.message_set.get(flag=Message.RESOLUTION, turn=1).content
		# Resolve yet another turn
		self.g.resolve_current_turn()

		# Launch information run, and retrieve all users datas.
		o2 = InformationRunOrder(
			target=self.p,
			player=p2,
			additional_percents=10,
		)
		o2.save()
		self.g.resolve_current_turn()

		p2_m = p2.message_set.get(flag=Message.PRIVATE_MESSAGE).content

		self.assertIn("Tour 1", p2_m)
		self.assertIn("Tour 2", p2_m)
		self.assertNotIn("Tour 3", p2_m)  # Current turn not included

		self.assertIn(p_m, p2_m)
