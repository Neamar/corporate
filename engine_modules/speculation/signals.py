# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order, post_create
from engine.exceptions import OrderNotAvailable
from engine_modules.corporation.models import Corporation
from engine_modules.speculation.models import Derivative, CorporationSpeculationOrder, DerivativeSpeculationOrder


@receiver(post_create, sender=Corporation)
def create_derivatives(sender, instance, **kwargs):
	if instance.base_corporation.derivative is not None:
		d, _ = Derivative.objects.get_or_create(name=instance.base_corporation.derivative, game=instance.game)
		d.corporations.add(instance)


def limit_speculation_by_influence(player):
	if CorporationSpeculationOrder.objects.filter(player=player, turn=player.game.current_turn).count() + DerivativeSpeculationOrder.objects.filter(player=player, turn=player.game.current_turn).count() >= player.influence.level:
		raise OrderNotAvailable("Pas assez d'influence pour spéculer à nouveau ce tour-ci.")


@receiver(validate_order, sender=CorporationSpeculationOrder)
def limit_corporation_speculation_by_influence(sender, instance, **kwargs):
	"""
	You can't speculate more than {{influence}} share per turn
	"""
	limit_speculation_by_influence(instance.player)


@receiver(validate_order, sender=DerivativeSpeculationOrder)
def limit_derivative_speculation_by_influence(sender, instance, **kwargs):
	"""
	You can't speculate more than {{influence}} share per turn
	"""
	limit_speculation_by_influence(instance.player)


@receiver(validate_order, sender=CorporationSpeculationOrder)
def limit_corporate_speculation_amount_by_influence(sender, instance, **kwargs):
	"""
	A speculation can't be more than {{influence}} * MAX_AMOUNT_SPECULATION ¥ per turn
	"""
	if instance.investment > instance.player.influence.level * sender.MAX_AMOUNT_SPECULATION:
		raise OrderNotAvailable("Pas assez d'influence pour spéculer un tel montant. (montant max : %s)" % (instance.player.influence.level * 50))


@receiver(validate_order, sender=DerivativeSpeculationOrder)
def limit_derivative_speculation_amount_by_influence(sender, instance, **kwargs):
	"""
	A speculation can't be more than {{influence}} * MAX_AMOUNT_SPECULATION ¥ per turn
	"""
	if instance.investment > instance.player.influence.level * sender.MAX_AMOUNT_SPECULATION:
		raise OrderNotAvailable("Pas assez d'influence pour spéculer un tel montant. (montant max : %s)" % (instance.player.influence.level * 50))
