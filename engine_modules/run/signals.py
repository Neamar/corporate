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
	if instance.has_RSEC_bonus and RunOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn, has_RSEC_bonus=True).count() >= 2:
		raise OrderNotAvailable("Seul la première run peut avoir la réduction de 'Réforme de la sécurité'.")
