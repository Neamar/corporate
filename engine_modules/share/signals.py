# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import IntegrityError

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable
from engine_modules.share.models import Share
from engine_modules.share.orders import BuyShareOrder


@receiver(validate_order, sender=BuyShareOrder)
def limit_buy_share_by_influence(sender, instance, **kwargs):
	"""
	You can't buy more than {{influence}} share per turn
	"""
	if BuyShareOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).count() >= instance.player.influence.level:
		raise OrderNotAvailable("Pas assez d'influence pour acheter à nouveau des parts ce tour-ci.")


@receiver(pre_save, sender=Share)
def set_share_turn(sender, instance, **kwargs):
	"""
	Automatically set share turn to current game turn when creating a share
	"""
	if not instance.pk:
		instance.turn = instance.player.game.current_turn
	else:
		raise IntegrityError("Can't update share.")


@receiver(pre_save, sender=Share)
def check_share_integrity(sender, instance, **kwargs):
	"""
	Check games matches
	"""
	if instance.player.game != instance.corporation.game:
		raise IntegrityError("Player and Corporation game does not match.")
