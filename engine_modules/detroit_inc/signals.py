# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable
from engine_modules.detroit_inc.models import DIncVoteOrder


@receiver(validate_order, sender=DIncVoteOrder)
def limit_dinc_order(sender, instance, **kwargs):
	"""
	Can't vote twice the same turn
	"""
	if DIncVoteOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Vous ne pouvez pas rejoindre deux coalitions dans le même tour.")
