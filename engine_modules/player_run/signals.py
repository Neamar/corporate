# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from engine.models import Player, Order
from engine_modules.corporation.models import Corporation
from engine_modules.player_run.models import InformationOrder


@receiver(m2m_changed)
def information_m2m_changed(action, instance, model, pk_set, **kwargs):
	if action == "post_add":
		update_instance = False
		price_all_orders = 0
		orders = Order.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exclude(pk=instance.pk)
		for order in orders:
			price_all_orders += order.cost

		for key in pk_set:
			if model == Player:
				if price_all_orders + instance.cost + InformationOrder.PLAYER_COST > instance.player.money:
					instance.player_targets.remove(key)
				else:
					update_instance = True
					instance.cost += InformationOrder.PLAYER_COST
			elif model == Corporation:
				if price_all_orders + instance.cost + InformationOrder.CORPORATION_COST > instance.player.money:
					instance.corporation_targets.remove(key)
				else:
					update_instance = True
					instance.cost += InformationOrder.CORPORATION_COST

		if update_instance is True:
			instance.save()
