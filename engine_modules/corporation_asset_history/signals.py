# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import post_create
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory

@receiver(post_create, sender=Corporation)
def initialise_asset_history(sender, instance, **kwargs):
	"""
	Save the assets state of corporation at start of the game (turn 0)
	"""
	ah=AssetHistory(corporation=instance,assets=instance.assets,turn=0)
	ah.save()