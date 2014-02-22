from engine.testcases import EngineTestCase
from engine.models import Player
from messaging.models import Message
from engine_modules.player_run.models import InformationRunOrder


class TaskTest(EngineTestCase):
	def test_information_run_success(self):
		"""
		Check we get a message with target player order
		"""

		from engine_modules.influence.models import BuyInfluenceOrder

		o = BuyInfluenceOrder(
			player=self.p
		)
		o.save()

		p2 = Player(game=self.g, money=self.initial_money)
		p2.save()

		o2 = InformationRunOrder(
			target=self.p,
			player=p2,
			additional_percents=10,
		)
		o2.save()

		self.g.resolve_current_turn()
		self.g.resolve_current_turn()

		p_m = self.p.message_set.get(flag=Message.RESOLUTION, turn=1).content
		p2_m = p2.message_set.get(flag=Message.PRIVATE_MESSAGE).content

		self.assertIn("Tour 1", p2_m)
		self.assertIn("Tour 2", p2_m)

		self.assertIn(p_m, p2_m)
