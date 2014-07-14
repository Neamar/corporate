# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable
from engine_modules.vote.models import VoteOrder


@receiver(validate_order, sender=VoteOrder)
def only_one_vote_per_turn(sender, instance, **kwargs):
	"""
	You can't vote more than once per turn
	"""
	if VoteOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Impossible de voter deux fois par tour")


@receiver(validate_order, sender=VoteOrder)
def check_existing_markets_for_up(sender, instance, **kwargs):
	"""
	The market need to be available on the corporation
	"""
	if not instance.corporation_up.corporationmarket_set.filter(market=instance.market_up).exists():
		raise ValidationError("This market is not available on this corporation.")


@receiver(validate_order, sender=VoteOrder)
def check_existing_markets_for_down(sender, instance, **kwargs):
	"""
	The market need to be available on the corporation
	"""
	if not instance.corporation_down.corporationmarket_set.filter(market=instance.market_down).exists():
		raise ValidationError("This market is not available on this corporation.")
