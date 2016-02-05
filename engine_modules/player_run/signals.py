# -*- coding: utf-8 -*-
from django.dispatch import receiver
from engine.models import Player, Order
from engine_modules.corporation.models import Corporation
from django.db.models.signals import m2m_changed
from engine_modules.player_run.models import InformationOrder
from django.core.exceptions import ValidationError
from django.db.models import Sum


@receiver(m2m_changed)
def information_m2m_changed(action, instance, model, **kwargs):
	if action == "pre_add":

		price_all_orders = Order.objects.filter(player=instance.player, turn=instance.player.game.current_turn).annotate(total_price=Sum('cost'))[0].total_price
		if model == Player:
			if price_all_orders + instance.cost + InformationOrder.PLAYER_COST > instance.player.money:
				raise ValidationError(u"Vous n'avez pas assez d'argent pour lancer cette opération dans son intégralité")
		elif model == Corporation:
			if price_all_orders + instance.cost + InformationOrder.CORPORATION_COST > instance.player.money:
				raise ValidationError(u"Vous n'avez pas assez d'argent pour lancer cette opération dans son intégralité")
		else:
			instance.cost = instance.get_cost()
			instance.save()
