# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import post_create
from engine.models import Game
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory

@receiver(post_create, sender=Game)
def initialise_asset_history(sender, instance, **kwargs):
	"""
	Save the assets state of corporation at start of the game (turn 0)
	"""
	corporations = Corporation.objects.filter(game=instance)
	for corporation in corporations:
		ah=AssetHistory(corporation=corporation,assets=corporation.assets,turn=0)
		ah.save()