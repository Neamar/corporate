# -*- coding: utf-8 -*-
from django.dispatch import receiver
from engine.models import Player
from engine_modules.corporation.models import Corporation
from django.db.models.signals import m2m_changed
from engine_modules.player_run.models import InformationOrder
from django.core.exceptions import ValidationError


@receiver(m2m_changed)
def information_m2m_changed(action, instance, model, **kwargs):
	if action == "pre_add":
		if model == Player:
			if InformationOrder.PLAYER_COST > instance.player.money:
				raise ValidationError(u"Vous n'avez pas assez d'argent pour lancer cette run")
		elif model == Corporation:
			if InformationOrder.CORPORATION_COST > instance.player.money:
				raise ValidationError(u"Vous n'avez pas assez d'argent pour lancer cette run")
		else:
			instance.cost = instance.get_cost()
			instance.save()
