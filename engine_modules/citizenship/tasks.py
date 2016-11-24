# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask, OrderResolutionTask
from engine_modules.citizenship.models import Citizenship, CitizenshipOrder


class CreateCitizenshipTask(ResolutionTask):
	"""
	Create the Citizenship object for the turn
	"""
	RESOLUTION_ORDER = 0

	def run(self, game):
		new_citizenships = []
		past_citizenships = Citizenship.objects.filter(player__game=game, turn=game.current_turn - 1)
		for past_citizenship in past_citizenships:
			citizenship = Citizenship(player=past_citizenship.player, corporation=past_citizenship.corporation, turn=game.current_turn)
			new_citizenships.append(citizenship)
		Citizenship.objects.bulk_create(new_citizenships)


class CitizenshipTask(OrderResolutionTask):
	"""
	Update players citizenships
	"""
	RESOLUTION_ORDER = 1600
	ORDER_TYPE = CitizenshipOrder

tasks = (CreateCitizenshipTask, CitizenshipTask,)
