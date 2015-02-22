# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order, post_create
from engine.exceptions import OrderNotAvailable
from engine.models import Player
from engine_modules.influence.models import Influence, BuyInfluenceOrder


@receiver(post_create, sender=Player)
def auto_create_player_influence(sender, instance, **kwargs):
	"""
	Create influence model for new player
	"""
	Influence(player=instance).save()


@receiver(validate_order, sender=BuyInfluenceOrder)
def only_one_influence_per_turn(sender, instance, **kwargs):
	"""
	You can't buy more than one influence per turn
	This is kinda like some "unique_together" constraint, except on inherited models.
	"""
	if BuyInfluenceOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Impossible d'acheter de l'influence deux fois par tour.")
