# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from engine.dispatchs import post_create

from engine.models import Game
from engine_modules.corporation.models import BaseCorporation, Corporation


@receiver(post_create, sender=Game)
def auto_create_corporation(sender, instance, **kwargs):
	"""
	Create influence model for new player
	Takes all the Base corporations and create corresponding Corporations
	"""
	base_corporations = BaseCorporation.retrieve_all()
	for base_corporation in base_corporations:
	#Temporary, only for debug, don't freak out, I'll remove it later
		print "Corporation : %s" %base_corporation.name
		Corporation(
			base_corporation_slug=base_corporation.slug,
			game=instance,
			assets=base_corporation.initials_assets
		).save()


@receiver(pre_save, sender=Corporation)
def corporation_negative_assets(sender, instance, **kwargs):
	"""
	Negative assets == 0 assets.
	This ensure integrity constraints on DB level.
	The corporation will then be deleted in crash_corporation_without_assets
	"""
	if instance.assets <= 0:
		instance.assets = 0


@receiver(post_save, sender=Corporation)
def crash_corporation_without_assets(sender, instance, **kwargs):
	"""
	A corporation without any assets gets deleted
	"""
	if instance.assets <= 0:
		instance.delete()
