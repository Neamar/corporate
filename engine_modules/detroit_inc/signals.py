# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order, post_create
from engine.exceptions import OrderNotAvailable
from engine.decorators import sender_instance_of
from engine_modules.run.models import RunOrder
from engine_modules.detroit_inc.models import DIncVoteOrder
from engine_modules.detroit_inc.decorators import expect_coalition


@receiver(validate_order, sender=DIncVoteOrder)
def limit_dinc_order(sender, instance, **kwargs):
	"""
	Can't vote twice the same turn
	"""
	if DIncVoteOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Vous ne pouvez pas rejoindre deux coalitions dans le même tour.")


@receiver(post_create)
@sender_instance_of(RunOrder)
@expect_coalition(DIncVoteOrder.RSEC)
def enforce_dinc_rsec(sender, instance, **kwargs):
	"""
	When RSEC line is active,
	* +20%% for RSEC players
	* -20%% for CONS players
	"""
	player_vote = instance.player.get_last_dinc_coalition()
	if player_vote == DIncVoteOrder.CONS:
		instance.hidden_percents -= 2
		instance.save()
	elif player_vote == DIncVoteOrder.RSEC:
		instance.hidden_percents += 2
		instance.save()
