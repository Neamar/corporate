# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from engine.models import Player, Order
from engine_modules.player_run.models import InformationOrder


@receiver(m2m_changed, sender=InformationOrder.player_targets.through)
def information_player_m2m_changed(action, instance, model, pk_set, sender, **kwargs):
	if action == "post_add":
		# We put the minimum cost (InformationOrder.CORPORATION_COST) by default because we don't want this order to be bought if you have less
		# Here we calculate the real cost. To do so we need to start at 0. This function is called once for players and once for corporation in that order.
		# If the order change, this calculation will be wrong !
		if model == Player:
			instance.cost = 0
		price_all_orders = 0
		orders = Order.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exclude(pk=instance.pk)
		for order in orders:
			price_all_orders += order.cost

		for key in pk_set:
			if price_all_orders + instance.cost + InformationOrder.PLAYER_COST > instance.player.money:
				instance.player_targets.remove(key)
			else:
				instance.cost += InformationOrder.PLAYER_COST

		instance.save()


@receiver(m2m_changed, sender=InformationOrder.corporation_targets.through)
def information_corporation_m2m_changed(action, instance, model, pk_set, sender, **kwargs):
	if action == "post_add":
		# We put the minimum cost (InformationOrder.CORPORATION_COST) by default because we don't want this order to be bought if you have less
		# Here we calculate the real cost. To do so we need to start at 0. This function is called once for players and once for corporation in that order.
		# If the order change, this calculation will be wrong != 0
		price_all_orders = 0
		orders = Order.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exclude(pk=instance.pk)
		for order in orders:
			price_all_orders += order.cost

		for key in pk_set:
			if price_all_orders + instance.cost + InformationOrder.CORPORATION_COST > instance.player.money:
				instance.corporation_targets.remove(key)
			else:
				instance.cost += InformationOrder.CORPORATION_COST

		instance.save()
