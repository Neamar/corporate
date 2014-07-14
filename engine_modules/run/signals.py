# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine.decorators import sender_instance_of
from engine.exceptions import OrderNotAvailable
from engine_modules.run.models import RunOrder


@receiver(validate_order)
@sender_instance_of(RunOrder)
def only_influence_bonus_per_turn(sender, instance, **kwargs):
	"""
	You can't use more 30%% bonuses than you have influence
	"""
	if instance.has_influence_bonus and RunOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn, has_influence_bonus=True).count() >= instance.player.influence.level:
		raise OrderNotAvailable("Impossible d'affecter la remise de 300k: vous n'avez pas assez d'influence corporatiste.")


@receiver(validate_order, sender=RunOrder)
def max_is_90(sender, instance, **kwargs):
	"""
	You can't have more than 90% probability of success
	"""
	if instance.get_success_probability() > 90:
		raise OrderNotAvailable("Impossible d'avoir plus de 90% de réussite sur une run.")
