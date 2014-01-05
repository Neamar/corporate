# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory



class SaveTurnHistoryTask(ResolutionTask):
	"""
	Save the assets of all corporations at the end of the turn
	"""
	RESOLUTION_ORDER = 1000

	def run(self, game):
		corporations = Corporation.objects.filter(game=game)
		turn=game.current_turn
		for corporation in corporations:
			ah=AssetHistory(corporation=corporation,assets=corporation.assets,turn=turn)
			ah.save()


class SendGlobalMessageTask(ResolutionTask):
	"""
	At the end of the turn, sent a message on what happend this turn
	"""

	RESOLUTION_ORDER = 1100

	def run(self, game):

		"""
		Create the general note for corporate classement
		"""
		#Ajout d'une note Construction du classement des corpo avec delta du tour précédent.
		classement=""
		position=1
		corporations = Corporation.objects.filter(game=game).order_by('-assets')
		for corporation in corporations:
			classement+="\n%s- %s : %s" % (position, corporation.base_corporation.name,corporation.assets)
			#add delta only if the corpo did exists the previous turn
			if AssetHistory.objects.filter(corporation=corporation,turn=(game.current_turn-1)).count()>0:
				classement+= " (%s)" % AssetHistory.objects.get(corporation=corporation,turn=(game.current_turn-1)).assets
			position+=1
		game.add_note(title="Classement corporatiste", content=classement)

tasks = (SaveTurnHistoryTask, SendGlobalMessageTask)
