# -*- coding: utf-8 -*-
from django.dispatch import receiver
from engine.dispatchs import post_create

from engine.models import Game
from engine_modules.corporation.models import BaseCorporation, Corporation


@receiver(post_create, sender=Game)
def auto_create_corporation(sender, instance, **kwargs):
	"""
	Create influence model for new player
	"""
	base_corporations = BaseCorporation.objects.all()
	for base_corporation in base_corporations:
		Corporation(
			base_corporation=base_corporation,
			game=instance,
			assets=10
		).save()
