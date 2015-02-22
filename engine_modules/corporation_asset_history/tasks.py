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
		ahs = []
		for corporation in corporations:
			ah = AssetHistory(
				corporation=corporation,
				assets=corporation.assets,
				turn=game.current_turn)
			ahs.append(ah)
		AssetHistory.objects.bulk_create(ahs)

tasks = (SaveCorporationAssetTask, )
