# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable
from engine_modules.speculation.models import SpeculationOrder

@receiver(validate_order, sender=SpeculationOrder)
def limit_buy_share_by_influence(sender, instance, **kwargs):
	"""
	You can't speculate more than {{influence}} share per turn
	"""
	if SpeculationOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).count() >= instance.player.influence.level:
		raise OrderNotAvailable("Pas assez d'influence pour spéculer à nouveau ce tour-ci.")
