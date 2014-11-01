# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order, post_create
from engine.exceptions import OrderNotAvailable
from engine_modules.speculation.models import CorporationSpeculationOrder


@receiver(validate_order, sender=CorporationSpeculationOrder)
def limit_speculation_amount_by_influence(sender, instance, **kwargs):
	"""
	Total speculation amount can't be more than {{influence}} * MAX_AMOUNT_SPECULATION ¥ per turn
	"""
	if instance.investment is None:
		return

	current_speculations = CorporationSpeculationOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn)
	current_speculation_amount = sum([speculation.investment for speculation in current_speculations])

	if instance.investment + current_speculation_amount > instance.player.influence.level * sender.MAX_AMOUNT_SPECULATION:
		raise OrderNotAvailable("Pas assez d'influence pour spéculer un tel montant (montant max : %s)." % (instance.player.influence.level * instance.MAX_AMOUNT_SPECULATION - instance.investment))


@receiver(post_create, sender=CorporationSpeculationOrder)
def decrease_ratio_when_speculating_first_last(sender, instance, **kwargs):
	"""
	You get less money for speculating on first / last
	"""
	if instance.rank == 1 or instance.rank == instance.player.game.corporation_set.count():
		instance.on_win_ratio -= 2
		instance.save()


@receiver(validate_order, sender=CorporationSpeculationOrder)
def forbid_nonexisting_rank(sender, instance, **kwargs):
	"""
	Can't speculate on non-existing rank
	"""
	if instance.rank > instance.player.game.corporation_set.count():
		raise OrderNotAvailable("Aucune corporation ne peut être à ce rang.")
