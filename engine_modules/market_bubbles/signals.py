# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable
from engine_modules.market_bubbles.models import MarketBubble
from engine_modules.market.models import Market, CorporationMarket

@receiver(pre_save, sender=MarketBubble)
def unique_domination_bubble(sender, instance, **kwargs):
	"""
	If instance is a domination bubble (value = 1), then check there isn't already one
	"""

	if instance.value != 1:
		return

	Bubbles = MarketBubble.objects.all()
	bubbles = MarketBubble.objects.filter(corporation__game=instance.corporation.game, turn=instance.turn, market=instance.market)
	if len(bubbles) > 0:
		raise ValidationError(u"Il ne peut pas y avoir plus d'une bulle pour le marché '%s'" %instance.market.name)

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


