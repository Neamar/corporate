# -*- coding: utf-8 -*-
from django.dispatch import receiver

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
