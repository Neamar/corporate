from engine.testcases import EngineTestCase
from engine.models import Player
from engine_modules.player_run.models import InformationOrder
from logs.models import Log
from django.db.models import Q


class InformationRunOrderTest(EngineTestCase):
	def setUp(self):
		super(InformationRunOrderTest, self).setUp()

		self.p2 = Player(game=self.g, secrets="Some nasty sfuff")
		self.p2.save()

		from engine_modules.corporation_run.models import SabotageOrder

		# Initial setup, create logs we'll use later.
		o = SabotageOrder(
			player=self.p2,
			target_corporation_market=self.c.get_random_corporation_market_among_bests()
		)
		o.save()

		self.io = InformationOrder(
			player=self.p,
		)
		self.io.clean()
		self.io.save()

	def test_no_information_gives_no_logs(self):
		"""
		No information run == no logs for target player.
		Just a sanity check
		"""
		self.io.delete()

		self.g.resolve_current_turn()

		# Sanity check: no information run, no knownloedge on player 2 action
		self.assertEqual(len(Log.objects.for_player(self.p2, self.p, self.g.current_turn)), 0)

	def test_information_on_player_gives_logs(self):
		"""
		Information run gives information about the sabotage
		"""
		self.io.player_targets.add(self.p2)
		self.g.resolve_current_turn()

		self.assertEqual(len(Log.objects.for_player(self.p2, self.p, self.g.current_turn).filter(Q(event_type=self.g.OPE_SABOTAGE) | Q(event_type=self.g.OPE_SABOTAGE_FAIL))), 1)

	def test_double_information_gives_logs(self):
		"""
		Sending the same information run twice should not crash (not add concernedplayer twice)
		"""
		self.io.player_targets.add(self.p2)
		self.io2 = InformationOrder(
			player=self.p,
			additional_percents=10,
		)
		self.io2.clean()
		self.io2.save()
		self.io2.player_targets.add(self.p2)

		self.g.resolve_current_turn()

		self.assertEqual(len(Log.objects.for_player(self.p2, self.p, self.g.current_turn).filter(Q(event_type=self.g.OPE_SABOTAGE) | Q(event_type=self.g.OPE_SABOTAGE_FAIL))), 1)

	def test_informations_on_corporations_gives_logs(self):
		self.io.corporation_targets.add(self.c)

		self.g.resolve_current_turn()

	def test_information_on_corporation_give_logs(self):
		"""
		We get information about the corporation
		"""
		self.io.corporation_targets.add(self.c)
		self.g.resolve_current_turn()

		self.assertEqual(len(Log.objects.for_player(self.p2, self.p, self.g.current_turn)), 1)

	# def test_information_on_citizenship_auto(self):
	# 	"""

	# 	"""
	# 	s = Share(
	# 		player=self.p,
	# 		corporation=self.c
	# 	)
	# 	s.save()

	# 	o = CitizenshipOrder(
	# 		player=self.p,
	# 		corporation=self.c
	# 	)
	# 	o.clean()
	# 	o.save()

	# 	self.g.resolve_current_turn()

	# 	self.assertEqual(len(Log.objects.for_player(self.p2, self.p, self.g.current_turn)), 1)
