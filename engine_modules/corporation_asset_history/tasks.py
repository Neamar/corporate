# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from engine_modules.corporation_asset_history.models import AssetHistory


class SaveCorporationAssetTask(ResolutionTask):
	"""
	Save the assets of all corporations after the turn resolution
	"""
	RESOLUTION_ORDER = 650

	def run(self, game):
		corporations = game.corporation_set.all()
		for corporation in corporations:
			ah = AssetHistory(
				corporation=corporation,
				assets=corporation.assets,
				turn=game.current_turn)
			ah.save()

tasks = (SaveCorporationAssetTask, )
