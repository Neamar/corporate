# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order, post_create
from engine.exceptions import OrderNotAvailable
from engine.decorators import sender_instance_of
from engine_modules.mdc.models import MDCVoteOrder
from engine_modules.corporation_run.models import OffensiveRunOrder
from engine_modules.player_run.models import InformationOrder
from engine_modules.mdc.decorators import expect_coalition


@receiver(validate_order, sender=MDCVoteOrder)
def limit_mdc_order(sender, instance, **kwargs):
	"""
	Can't vote twice the same turn
	"""
	if MDCVoteOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Vous ne pouvez pas rejoindre deux coalitions dans le même tour.")


@receiver(post_create)
@sender_instance_of(OffensiveRunOrder, InformationOrder)
@expect_coalition(MDCVoteOrder.OPCL)
def enforce_mdc_opcl(sender, instance, **kwargs):
	"""
	When OPCL line is active,
	* +20%% for OPCL players
	* -20%% for CONS players
	"""
	player_vote = instance.player.get_last_mdc_coalition()
	if player_vote == MDCVoteOrder.CONS:
		instance.hidden_percents -= 2
		instance.save()
	elif player_vote == MDCVoteOrder.OPCL:
		instance.hidden_percents += 2
		instance.save()
