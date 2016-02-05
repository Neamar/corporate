# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.db.models import Sum

from engine.models import Player, Order
from engine_modules.corporation.models import Corporation
from engine_modules.player_run.models import InformationOrder


@receiver(m2m_changed)
def information_m2m_changed(action, instance, model, **kwargs):
	if action == "post_add":
		price_all_orders = Order.objects.filter(player=instance.player, turn=instance.player.game.current_turn).annotate(total_price=Sum('cost'))[0].total_price
		if model == Player:
			if price_all_orders + instance.cost + InformationOrder.PLAYER_COST > instance.player.money:
				instance.player_targets.remove(model)
			else:
				instance.cost += InformationOrder.PLAYER_COST
				instance.save()
		elif model == Corporation:
			if price_all_orders + instance.cost + InformationOrder.CORPORATION_COST > instance.player.money:
				instance.corporation_targets.remove(model)
			else:
				instance.cost += InformationOrder.CORPORATION_COST
				instance.save()
