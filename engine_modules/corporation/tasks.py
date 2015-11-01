# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from engine_modules.citizenship.models import Citizenship


class CrashCorporationTask(ResolutionTask):
	"""
	Let's crash corporations that didn't make it through the turn
	"""
	RESOLUTION_ORDER = 850

	def run(self, game):
		corporations_to_crash = game.corporation_set.filter(assets__lte=0)

		if not corporations_to_crash:
			return

		# We apply the crashed state on each corporation
		for corporation in corporations_to_crash:
			corporation.crash_turn = game.current_turn
			corporation.save()

		ladder = game.get_ladder()
		# Then, we apply the crashed effects only on alives corporations
		for corporation in corporations_to_crash:
			corporation.on_crash_effect(ladder)
			game.add_event(event_type=game.CORPORATION_CRASHED, data={"corporation": corporation.base_corporation.name}, corporation=corporation)

		# get citizenship to delete
		citizenship_to_delete = Citizenship.objects.filter(corporation__in=corporations_to_crash, turn=game.current_turn)
		for citizenship in citizenship_to_delete:
			# create a game_event for each removed citizenship
			game.add_event(event_type=game.REMOVE_CITIZENSHIP, data={"player": citizenship.player.name, "corporation": citizenship.corporation.base_corporation.name}, corporation=citizenship.corporation, players=[citizenship.player])
			# remove the citizenship
			citizenship.corporation = None
			citizenship.save()

		
tasks = (CrashCorporationTask,)
