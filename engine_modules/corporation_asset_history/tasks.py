# -*- coding: utf-8 -*-
from engine.tasks import ResolutionTask
from engine_modules.corporation_asset_history.models import AssetHistory


class SaveCorporationAssetTask(ResolutionTask):
	"""
	Save the assets of all corporations after the turn resolution
	"""
	RESOLUTION_ORDER = 1000

	def run(self, game):
		corporations = game.corporation_set.all()
		for corporation in corporations:
			ah = AssetHistory(
				corporation=corporation,
				assets=corporation.assets,
				turn=game.current_turn)
			ah.save()


class BuildCorporationRankingTask(ResolutionTask):
	"""
	Build the ranking between each corporation
	"""

	RESOLUTION_ORDER = 1100

	def run(self, game):
		"""
		Create the note for corporation rankings
		"""

		content = ""
		corporations = game.corporation_set.order_by('-assets')
		for rank, corporation in enumerate(corporations):
			previous_turn_assets = corporation.assethistory_set.get(turn=game.current_turn - 1).assets
			content += "%s- %s : %s  (%+d)\n" % (rank + 1, corporation.base_corporation.name, corporation.assets, corporation.assets - previous_turn_assets)

		game.add_note(category="Classement corporatiste", content=content)

tasks = (SaveCorporationAssetTask, BuildCorporationRankingTask)
