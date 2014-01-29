# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable
from engine_modules.speculation.models import CorporationSpeculationOrder

@receiver(validate_order, sender=CorporationSpeculationOrder)
def limit_speculation_by_influence(sender, instance, **kwargs):
	"""
	You can't speculate more than {{influence}} share per turn
	"""
	if CorporationSpeculationOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).count() >= instance.player.influence.level:
		raise OrderNotAvailable("Pas assez d'influence pour spéculer à nouveau ce tour-ci.")

@receiver(validate_order, sender=CorporationSpeculationOrder)
def limit_speculation_amount_by_influence(sender, instance, **kwargs):
	"""
	A speculation can't be more than {{influence}} * 50 000 ny per turn
	"""
	if instance.investment > instance.player.influence.level * 50:
		raise OrderNotAvailable("Pas assez d'influence pour spéculer un tel montant. (montant max : %s)" % instance.player.influence.level * 50)
