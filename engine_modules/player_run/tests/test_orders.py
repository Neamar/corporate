from engine_modules.corporation_run.tests.test_orders import RunOrdersTest
from engine.models import Player
from engine_modules.player_run.models import InformationOrder
from logs.models import Log


class InformationRunOrderTest(RunOrdersTest):
	def setUp(self):
		super(InformationRunOrderTest, self).setUp()

		self.p2 = Player(game=self.g, secrets="Some nasty sfuff")
		self.p2.save()
		citizenship = self.p2.citizenship
		citizenship.corporation = self.c
		citizenship.save()

		from engine_modules.corporation_run.models import SabotageOrder

		# Initial setup, create logs we'll use later.
		o = SabotageOrder(
			player=self.p2,
			target_corporation_market=self.c.get_random_corporation_market_among_bests()
		)
		o.save()

		self.io = InformationOrder(
			target=self.p2,
			player=self.p,
			additional_percents=10,
		)
		self.io.clean()
		self.io.save()

	def test_no_information_gives_no_logs(self):
		"""
		No information run == no lgos for target player.
		Just a sanity check
		"""
		self.io.delete()

		self.g.resolve_current_turn()

		# Sanity check: no information run, no knownloedge on player 2 action
		self.assertEqual(len(Log.objects.for_player(self.p2, self.p, self.g.current_turn)), 0)

	def test_information_gives_logs(self):
		"""
		Information run gives information about the sabotage
		"""
		self.g.resolve_current_turn()

		self.assertEqual(len(Log.objects.for_player(self.p2, self.p, self.g.current_turn)), 1)

	def test_double_information_gives_logs(self):
		"""
		Sending the same information run twice should not crash (not add concernedplayer twice)
		"""
		self.io2 = InformationOrder(
			target=self.p2,
			player=self.p,
			additional_percents=10,
		)
		self.io2.clean()
		self.io2.save()

		self.g.resolve_current_turn()

		self.assertEqual(len(Log.objects.for_player(self.p2, self.p, self.g.current_turn)), 1)
