from engine.testcases import EngineTestCase
from engine.models import Player
from engine_modules.wiretransfer.models import WiretransferOrder
from messaging.models import Message


class WiretransterOrderTest(EngineTestCase):
	def setUp(self):
		super(WiretransterOrderTest, self).setUp()

		self.p2 = Player(game=self.g, money=self.initial_money)
		self.p2.save()

		self.wo = WiretransferOrder(
			player=self.p,
			recipient=self.p2,
			amount=1
		)

	def test_wiretransfer_immediate(self):
		"""
		Wiretransfer sends money immediately
		"""
		self.wo.save()

		# Effect should be immediate
		self.assertEqual(self.reload(self.p).money, self.initial_money - self.wo.amount)
		self.assertEqual(self.reload(self.p2).money, self.initial_money + self.wo.amount)

		# Wiretransfer should not be saved in DB
		self.assertIsNone(self.wo.pk)

	def test_wiretransfer_message(self):
		"""
		Wiretransfer sends a message to both players
		"""
		self.wo.save()

		m = Message.objects.get()
		self.assertEqual(m.title, "Transfert d'argent")
		self.assertEqual(m.flag, Message.CASH_TRANSFER)
		self.assertIn(self.wo.player.name, m.content)
		self.assertIn(self.wo.recipient.name, m.content)
		self.assertIn(str(self.wo.amount), m.content)
