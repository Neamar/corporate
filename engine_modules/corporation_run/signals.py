# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.decorators import sender_instance_of
from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable

from engine_modules.corporation_run.models import OffensiveCorporationRunOrderWithStealer
from django.core.exceptions import ValidationError


@receiver(validate_order)
@sender_instance_of(OffensiveCorporationRunOrderWithStealer)
def target_stealer_differ(sender, instance, **kwargs):
	"""
	Datasteal / Extraction: target and stealer must be different
	"""
	if not hasattr(instance, 'target_corporation_market'):
		return

	if instance.target_corporation == instance.stealer_corporation:
		raise OrderNotAvailable(u"La cible et le bénéficiaire doivent être différents !")


@receiver(validate_order)
@sender_instance_of(OffensiveCorporationRunOrderWithStealer)
def both_have_target_corporation_market(sender, instance, **kwargs):
	"""
	Datasteal / Extraction: The stealer must have assets on the target market
	"""

	if not hasattr(instance, 'target_corporation_market'):
		return

	if instance.target_corporation_market.market.name not in instance.stealer_corporation.base_corporation.markets.keys():
		raise ValidationError(u"Le marché « %s » n'est pas présent sur %s." % (instance.target_corporation_market.market.name, instance.stealer_corporation.base_corporation.name))


@receiver(validate_order)
@sender_instance_of(OffensiveCorporationRunOrderWithStealer)
def target_above_stealer(sender, instance, **kwargs):
	"""
	The target in a offensive run must have more assets than the stealer on the target market
	"""

	if not hasattr(instance, 'target_corporation_market'):
		return

	target_value = instance.target_corporation_market.value
	stealer_value = instance.stealer_corporation_market.value

	if target_value < stealer_value:
		raise ValidationError(u"Le marché %s de %s est plus bas que celui de %s" % (instance.target_corporation_market.market.name, instance.target_corporation.base_corporation.name, instance.stealer_corporation.base_corporation.name))
