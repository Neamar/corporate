# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import post_create
from engine_modules.share.models import Share


@receiver(post_create, sender=Share)
def set_share_turn(sender, instance, **kwargs):
	"""
	Automatically set share turn to current game turn
	"""
	instance.turn = instance.player.game.current_turn
	instance.save()
