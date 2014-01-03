from engine.tasks import ResolutionTask
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory

class SaveTurnHistory(ResolutionTask):
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

tasks = (SaveTurnHistory, )