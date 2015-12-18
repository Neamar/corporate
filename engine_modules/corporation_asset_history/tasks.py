# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from engine_modules.corporation_asset_history.models import AssetHistory


class SaveCorporationAssetTask(ResolutionTask):
	"""
	Save the assets of all corporations after the turn resolution
	"""
	RESOLUTION_ORDER = 875

	def run(self, game):
		# We save corporation asset, even for the corporations which have crashed this turn
		corporations = game.corporation_set.all()
		ahs = []
		for corporation in corporations:
			print '%s - %s' % (corporation, corporation.assets)
			ah = AssetHistory(
				corporation=corporation,
				assets=corporation.assets,
				turn=game.current_turn)
			ahs.append(ah)
		AssetHistory.objects.bulk_create(ahs)

tasks = (SaveCorporationAssetTask, )

initialisation_tasks = (SaveCorporationAssetTask, )
