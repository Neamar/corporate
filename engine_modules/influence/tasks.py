# -*- coding: utf-8 -*-
from engine.tasks import InitTask, OrderResolutionTask
from engine_modules.influence.models import Influence, BuyInfluenceOrder


class CreateInfluenceTask(InitTask):
	"""
	Create the Influence object for the turn
	"""

	RESOLUTION_ORDER = 0

	def run(self, game):
		new_influences = []
		past_influences = Influence.objects.filter(turn=game.current_turn - 1)
		for past_influence in past_influences:
			influence = Influence(player=past_influence.player, turn=game.current_turn, level=past_influence.level)
			new_influences.append(influence)
		Influence.objects.bulk_create(new_influences)


class BuyInfluenceTask(OrderResolutionTask):
	"""
	Buy new Influence level
	"""
	RESOLUTION_ORDER = 1000
	ORDER_TYPE = BuyInfluenceOrder


tasks = (CreateInfluenceTask, BuyInfluenceTask,)
