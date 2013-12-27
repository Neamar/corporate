# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import pre_save

from engine_modules.share.models import Share


@receiver(pre_save, sender=Share)
def set_share_turn(sender, instance, **kwargs):
	"""
	Automatically set share turn to current game turn when creating a share
	"""
	if not instance.pk:
		instance.turn = instance.player.game.current_turn
