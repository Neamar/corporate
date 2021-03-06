# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import post_create, validate_order, start_event
from engine.exceptions import OrderNotAvailable

from engine_modules.citizenship.models import Citizenship, CitizenshipOrder
from engine.models import Player
from engine_modules.corporation.models import Corporation


@receiver(post_create, sender=Player)
def auto_create_player_citizenship(sender, instance, **kwargs):
	"""
	Create citizenship model for new player
	"""
	Citizenship(player=instance).save()


@receiver(validate_order, sender=CitizenshipOrder)
def limit_citizenship_order(sender, instance, **kwargs):
	"""
	Can't change citizenship 2 times in the same turn
	"""
	if CitizenshipOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Vous ne pouvez pas demander une citoyenneté deux fois dans le même tour.")


@receiver(validate_order, sender=CitizenshipOrder)
def stop_when_no_shares(sender, instance, **kwargs):
	"""
	Order should not be available when player has no shares at all
	"""
	if not instance.player.share_set.exists():
		raise OrderNotAvailable("Vous devez avoir une part dans une corporation pour en prendre la nationalité.")


@receiver(validate_order, sender=CitizenshipOrder)
def citizenship_need_one_share(sender, instance, **kwargs):
	"""
	You need at least one share to get a citizenship
	"""
	if not hasattr(instance, 'corporation'):
		return

	if not instance.player.share_set.filter(corporation=instance.corporation).exists():
		raise OrderNotAvailable("Vous devez avoir au moins une part dans la corporation dont vous souhaitez devenir citoyen.")


@receiver(start_event)
def add_citizenship_at_start(sender, instance, **kwargs):
	"""
	Create citizenship model for new player
	"""
	for player in instance.player_set.all():
		if player.starting_citizenship:
			# Créer la citoyenneté
			corporation = Corporation.objects.get(pk=player.starting_citizenship)
			instance.add_event(event_type=instance.ADD_CITIZENSHIP, turn=instance.current_turn - 1, data={"player": player.name, "corporation": corporation.base_corporation.name}, corporation=corporation, players=[player])
			citizenship = player.citizenship_set.get(turn=instance.current_turn - 1)
			citizenship.corporation = corporation
			citizenship.save()
