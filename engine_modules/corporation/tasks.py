# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from engine_modules.citizenship.models import Citizenship
from logs.models import Log
from engine_modules.corporation.models import Corporation


class CrashCorporationTask(ResolutionTask):
	"""
	Let's crash corporations that didn't make it through the turn
	"""
	RESOLUTION_ORDER = 850

	def run(self, game):
		corporations_to_crash = list(game.corporation_set.filter(assets__lte=0))

		if not corporations_to_crash:
			return

		first_crash_phoenix = False
		# Handle the case of phoenix part 1
		for corporation in corporations_to_crash:
			if corporation.base_corporation.phoenix == 1:
				# avoid others crashed effects to apply on Phoenix
				corporation.crash_turn = game.current_turn
				corporation.save()
				# search if a crashed took place before
				previous_crash = Log.objects.filter(game=game, event_type=game.CORPORATION_CRASHED, corporation=corporation)
				if not previous_crash:
					first_crash_phoenix = True
					phoenix = corporation
				# create an event
				game.add_event(event_type=game.CORPORATION_CRASHED, data={"corporation": corporation.base_corporation.name}, corporation=corporation)
				# remove Phoenix of classic processs for crash
				corporations_to_crash.remove(corporation)

		# We apply the crashed state on each corporation
		for corporation in corporations_to_crash:
			corporation.crash_turn = game.current_turn
			corporation.save()

		ladder = game.get_ladder()
		# Then, we apply the crashed effects only on alives corporations
		for corporation in corporations_to_crash:
			corporation.on_crash_effect(ladder)
			# We create the event
			game.add_event(event_type=game.CORPORATION_CRASHED, data={"corporation": corporation.base_corporation.name}, corporation=corporation)

		# Handle the case of phoenix part 2
		if first_crash_phoenix:
			# We remove the crashed state on Phoenix. We need that because Phoenix applies an effect on itself and effects don't apply on crashed corporations
			phoenix.crash_turn = None
			phoenix.save()
			# We apply crashed effect
			phoenix.on_crash_effect(ladder)
			# get the new assets of Phoenix. If <= 0, we apply the crashed state again
			phoenix = Corporation.objects.get(pk=phoenix.pk)
			if phoenix.assets <= 0:
				# Remove crashed effect. We put it in the first place to avoid others crashed effects to appy on Phoenix
				phoenix.crash_turn = game.current_turn
				phoenix.save()

		# get citizenship to delete
		citizenship_to_delete = Citizenship.objects.filter(corporation__crash_turn=game.current_turn, turn=game.current_turn)
		for citizenship in citizenship_to_delete:
			# create a game_event for each removed citizenship
			game.add_event(event_type=game.REMOVE_CITIZENSHIP, data={"player": citizenship.player.name, "corporation": citizenship.corporation.base_corporation.name}, corporation=citizenship.corporation, players=[citizenship.player])
			# remove the citizenship
			citizenship.corporation = None
			citizenship.save()


tasks = (CrashCorporationTask,)
