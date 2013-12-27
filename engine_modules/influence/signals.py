# -*- coding: utf-8 -*-
from engine.dispatchs import validate_order
from django.dispatch import receiver
from engine.exceptions import OrderNotAvailable

from engine_modules.influence.orders import BuyInfluenceOrder


@receiver(validate_order, sender=BuyInfluenceOrder)
def buy_influence_order_require_money(sender, instance, **kwargs):
	"""
	Check player has enough money for this order
	"""
	if instance.get_cost() + instance.player.get_current_orders_cost() > instance.player.money:
		raise OrderNotAvailable("Pas assez d'argent pour lancer cet ordre.")
