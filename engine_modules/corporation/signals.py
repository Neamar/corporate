# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
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
			assets=base_corporation.initials_assets
		).save()


@receiver(post_save, sender=Corporation)
def crash_corporation_without_assets(sender, instance, **kwargs):
	"""
	A corporation without any assets gets deleted
	"""
	if instance.assets <= 0:
		instance.delete()
