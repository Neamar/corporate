# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable
from engine_modules.run.models import RunOrder


@receiver(validate_order, sender=RunOrder)
def only_influence_bonus_per_turn(sender, instance, **kwargs):
	"""
	You can't use more 30% bonuses than you have influence
	"""
	if RunOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).count() >= instance.player.influence.level:
		raise OrderNotAvailable("Impossible d'affecter le bonus de 30%: vous n'avez pas assez d'influence corporatiste.")
