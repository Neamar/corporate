# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError

from engine_modules.market_bubbles.models import MarketBubble
from engine_modules.market.models import CorporationMarket


@receiver(pre_save, sender=MarketBubble)
def unique_domination_bubble(sender, instance, **kwargs):
	"""
	If instance is a domination bubble (value = 1), then check there isn't already one
	"""

	if instance.value != 1:
		return

	bubbles = MarketBubble.objects.filter(corporation__game=instance.corporation.game, turn=instance.turn, market=instance.market).exclude(corporation=instance.corporation)
	if len(bubbles) > 0:
		raise ValidationError(u"Il ne peut pas y avoir plus d'une bulle pour le marché '%s'" % instance.market.name)


@receiver(pre_save, sender=MarketBubble)
def domination_in_corporations_markets(sender, instance, **kwargs):
	"""
	Check that the bubble's market is among the corporation's markets
	"""

	corporation_markets = []
	for cm in CorporationMarket.objects.filter(corporation=instance.corporation):
		corporation_markets.append(cm.market)
	if instance.market not in corporation_markets:
		raise ValidationError(u"La corporation %s ne peut pas dominer un marché où elle n'est pas présente")

# TODO: write a signal to prevent having a positive and a negative bubble on the same market for the same corporation
