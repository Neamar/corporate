# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable
from engine_modules.run.models import RunOrder


@receiver(validate_order)
def only_influence_bonus_per_turn(sender, instance, **kwargs):
	"""
	You can't use more 30% bonuses than you have influence
	"""
	if isinstance(instance, RunOrder):
		if instance.has_influence_bonus and RunOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).count() >= instance.player.influence.level:
			raise OrderNotAvailable("Impossible d'affecter le bonus de 30%: vous n'avez pas assez d'influence corporatiste.")


@receiver(validate_order, sender=RunOrder)
def max_is_90(sender, instance, **kwargs):
	"""
	You can't have more than 90% probability of success
	"""
	if instance.get_success_probability() > 90:
		raise OrderNotAvailable("Impossible d'avoir plus de 90% de réussite sur une run.")
