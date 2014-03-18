from engine.testcases import EngineTestCase
from engine.models import Player
from engine_modules.wiretransfer.models import WiretransferOrder


class WiretransterOrderTest(EngineTestCase):
	def setUp(self):
		super(WiretransterOrderTest, self).setUp()

		self.p2 = Player(game=self.g, money=self.initial_money)
		self.p2.save()

	def test_wiretransfer_immediate(self):
		"""
		Wiretransfer sends money immediately
		"""
		wo = WiretransferOrder(
			player=self.p,
			recipient=self.p2,
			amount=1
		)

		wo.save()

		# Effect should be immediate
		self.assertEqual(self.reload(self.p).money, self.initial_money - wo.amount)
		self.assertEqual(self.reload(self.p2).money, self.initial_money + wo.amount)

		# Wiretransfer should not be saved in DB
		self.assertIsNone(wo.pk)
