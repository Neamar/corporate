# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save

from engine.models import Game
from engine_modules.corporation.models import BaseCorporation, Corporation


@receiver(post_save, sender=Game)
def auto_create_corporation(sender, instance, created, **kwargs):
	"""
	Create influence model for new player
	"""
	if created:
		base_corporations = BaseCorporation.objects.all()
		for base_corporation in base_corporations:
			Corporation(
				base_corporation=base_corporation,
				game=instance,
				assets=10
			).save()
