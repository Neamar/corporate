# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine_modules.mdc.models import MDCVoteOrder
from engine.exceptions import OrderNotAvailable


@receiver(validate_order, sender=MDCVoteOrder)
def limit_mdc_order(sender, instance, **kwargs):
	"""
	Can't vote twice the same turn
	"""
	if MDCVoteOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Vous ne pouvez pas voter deux fois dans le même tour.")
