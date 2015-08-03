# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError

from engine_modules.market.models import CorporationMarket


@receiver(pre_save, sender=CorporationMarket)
def unique_domination_bubble(sender, instance, **kwargs):
	"""
	If instance has a bubble value above 1, then someone has tried to put several domination bubbles on it
	"""

	if instance.bubble_value > 1:
		raise ValidationError(u"Il ne peut pas y avoir plus d'une bulle pour le marché '%s'" % instance.market.name)
