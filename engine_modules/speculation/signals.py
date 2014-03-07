# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.decorators import sender_instance_of
from engine.dispatchs import validate_order, post_create
from engine.exceptions import OrderNotAvailable
from engine_modules.corporation.models import Corporation
from engine_modules.speculation.models import Derivative, CorporationSpeculationOrder, DerivativeSpeculationOrder


@receiver(post_create, sender=Corporation)
def create_derivatives(sender, instance, **kwargs):
	if instance.base_corporation.derivative is not None:
		d, _ = Derivative.objects.get_or_create(name=instance.base_corporation.derivative, game=instance.game)
		d.corporations.add(instance)


@receiver(validate_order)
@sender_instance_of(CorporationSpeculationOrder, DerivativeSpeculationOrder)
def limit_speculation_by_influence(sender, instance, **kwargs):
	"""
	You can't speculate more than {{influence}} share per turn
	"""
	player = instance.player
	if CorporationSpeculationOrder.objects.filter(player=player, turn=player.game.current_turn).count() + DerivativeSpeculationOrder.objects.filter(player=player, turn=player.game.current_turn).count() >= player.influence.level:
		raise OrderNotAvailable("Pas assez d'influence pour spéculer à nouveau ce tour-ci.")


@receiver(validate_order)
@sender_instance_of(CorporationSpeculationOrder, DerivativeSpeculationOrder)
def limit_speculation_amount_by_influence(sender, instance, **kwargs):
	"""
	A speculation can't be more than {{influence}} * MAX_AMOUNT_SPECULATION ¥ per turn
	"""
	if instance.investment > instance.player.influence.level * sender.MAX_AMOUNT_SPECULATION:
		raise OrderNotAvailable("Pas assez d'influence pour spéculer un tel montant (montant max : %s)." % (instance.player.influence.level * instance.MAX_AMOUNT_SPECULATION))


@receiver(post_create, sender=CorporationSpeculationOrder)
def decrease_ratio_when_speculating_first_last(sender, instance, **kwargs):
	"""
	You get less money for speculating on first / last
	"""
	if instance.rank == 1 or instance.rank == instance.player.game.corporation_set.count():
		instance.on_win_ratio -= 2
		instance.save()
