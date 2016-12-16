# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import IntegrityError

from engine.dispatchs import validate_order, start_event
from engine.exceptions import OrderNotAvailable
from engine_modules.share.models import Share, BuyShareOrder
from engine_modules.corporation.models import Corporation


@receiver(start_event)
def add_citizenship_at_start(sender, instance, **kwargs):
	"""
	Create citizenship model for new player
	"""
	print "citizenship"
	for player in instance.player_set.all():
		if player.starting_citizenship:
			# Créer l'ordre d'achat de part non supprimable
			corporation = Corporation.objects.get(pk=player.starting_citizenship)
			order = BuyShareOrder(
				player=player,
				corporation=corporation
			)
			order.cancellable = False
			order.save()


@receiver(validate_order, sender=BuyShareOrder)
def limit_buy_share_by_influence(sender, instance, **kwargs):
	"""
	You can't buy more than {{influence}} share per turn
	"""
	if BuyShareOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).count() >= instance.player.influence.level:
		raise OrderNotAvailable("Pas assez d'influence pour acheter à nouveau des parts ce tour-ci.")


@receiver(pre_save, sender=Share)
def set_share_turn(sender, instance, **kwargs):
	"""
	Automatically set share turn to current game turn when creating a share
	"""
	if not instance.pk:
		instance.turn = instance.player.game.current_turn
	else:
		raise IntegrityError("Can't update share.")


@receiver(pre_save, sender=Share)
def check_share_integrity(sender, instance, **kwargs):
	"""
	Check games matches
	"""
	if instance.player.game != instance.corporation.game:
		raise IntegrityError("Player and Corporation game does not match.")
