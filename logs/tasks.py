# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from engine.models import Player


class MoneyInformationTask(ResolutionTask):
	"""
	Inform players for their money next turn
	"""
	RESOLUTION_ORDER = 1100

	def run(self, game):
		"""
		Raise an event on each player
		"""
		all_players = Player.objects.filter(game=game)

		# Create a game event. This event must be triggered only after all actions changing money have been passed this turn.
		for player in all_players:
			game.add_event(event_type=game.MONEY_NEXT_TURN, data={"player": player.name, "money": player.money}, players=[player])

tasks = (MoneyInformationTask, )
