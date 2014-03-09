from engine.testcases import EngineTestCase
from engine.models import Player
from messaging.models import Message

class WiretransterOrderTest(EngineTestCase):
	def setUp(self):
		super(WiretransterOrderTest, self).setUp()

		self.p2 = Player(game=self.g, secrets="Some nasty sfuff")
		self.p2.save()

	def test_wiretransfer_immediate(self):
		"""
		Wiretransfer sends data immediately
		"""
		pass
