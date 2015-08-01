from engine.testcases import EngineTestCase
from engine.models import Game, Player
from logs.models import Logs, ConcernedPlayers


class SignalTest(EngineTestCase):
	def test_log_creation(self):
		"""
		Check a game_event creates a Logs in DB and a Many-To-Many with players
		"""
		self.p2 = Player(game=self.g, money=self.initial_money)
		self.p2.save()

		logs_before = Logs.objects.count()
		m2m_before = ConcernedPlayers.objects.count()

		self.g.add_event(event_type=Game.WIRETRANSFER, data=None, players=[self.p, self.p2])

		self.assertEqual(1, Logs.objects.count() - logs_before)
		self.assertEqual(2, ConcernedPlayers.objects.count() - m2m_before)
