# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import post_create, validate_order
from engine.exceptions import OrderNotAvailable

from engine_modules.citizenship.models import CitizenShip
from engine_modules.citizenship.orders import CitizenShipOrder
from engine.models import Player


@receiver(post_create, sender=Player)
def auto_create_player_citizenship(sender, instance, **kwargs):
	"""
	Create citizenship model for new player
	"""
	CitizenShip(player=instance).save()

@receiver(validate_order, sender=CitizenShipOrder)
def limit_citizenship_order(sender, instance, **kwargs):
	"""
	Can't change citizenship 2 times in the same turn
	"""
	if CitizenShipOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Vous ne pouvez pas demander une citoyenneté deux fois dans le même tour.")
