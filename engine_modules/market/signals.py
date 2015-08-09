# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from engine_modules.market.models import CorporationMarket


@receiver(pre_save, sender=CorporationMarket)
def unique_domination_bubble(sender, instance, **kwargs):
	"""
	If instance has a bubble value above 1, then someone has tried to put several domination bubbles on it
	"""

	if instance.bubble_value > 1:
		raise ValidationError(u"There can at most be one domination bubble for market '%s'" % instance.market.name)


# TODO: Add a test_signal testing this
@receiver(pre_save, sender=CorporationMarket)
def bubble_value_ok(sender, instance, **kwargs):
	"""
	Check that the field "bubble_value" is either -1 (negative bubble), 0 (no bubble), or 1 (domination bubble)
	"""

	if instance.bubble_value not in (c[0] for c in CorporationMarket.BUBBLE_VALUES):
		raise IntegrityError(u"A CorporationMarket should have a bubble_value of either -1 (negative bubble), 0 (no bubble), or 1 (domination bubble)")
