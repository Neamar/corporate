# -*- coding: utf-8 -*-
from django.dispatch import receiver


from engine.dispatchs import validate_order, post_create
from engine.exceptions import OrderNotAvailable
from engine.models import Player
from engine_modules.influence.models import Influence
from engine_modules.influence.orders import BuyInfluenceOrder


@receiver(validate_order, sender=BuyInfluenceOrder)
def buy_influence_order_require_money(sender, instance, **kwargs):
	"""
	Check player has enough money for this order
	"""
	if instance.get_cost() + instance.player.get_current_orders_cost() > instance.player.money:
		raise OrderNotAvailable("Pas assez d'argent pour lancer cet ordre.")


@receiver(post_create, sender=Player)
def auto_create_player_influence(sender, instance, **kwargs):
	"""
	Create influence model for new player
	"""
	Influence(player=instance).save()
