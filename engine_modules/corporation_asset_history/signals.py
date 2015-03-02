# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import post_create
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory


@receiver(post_create, sender=Corporation)
def initialize_asset_history(sender, instance, **kwargs):
	"""
	Save the corporation assets history at game start (turn 0)
	"""
	ah = AssetHistory(
		corporation=instance,
		assets=instance.assets,
		turn=0
	)
	ah.save()
