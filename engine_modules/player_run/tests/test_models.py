from engine.testcases import EngineTestCase
from engine_modules.player_run.models import InformationRunOrder
from engine.models import Player, Message

class TaskTest(EngineTestCase):
	"""
	Unit tests for Player's runs
	"""

	def test_information_run_success(self):
		from engine_modules.influence.models import BuyInfluenceOrder

		o = BuyInfluenceOrder(
			player=self.p
		)
		o.save()
		self.g.resolve_current_turn()
		m = self.p.message_set.filter(flag=Message.ORDER)[0]

		p2 = Player(game=self.g)
		p2.save()

		o2 = InformationRunOrder(
			target=self.p,
			player=p2,
		)
		o2.save()
		o2.resolve_successful()
		self.assertTrue(m.content in p2.message_set.all()[0].content)
