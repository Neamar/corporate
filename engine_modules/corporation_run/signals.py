# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.decorators import sender_instance_of
from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable

from engine_modules.corporation_run.models import DataStealOrder, ExtractionOrder
from django.core.exceptions import ValidationError


@receiver(validate_order)
@sender_instance_of(DataStealOrder, ExtractionOrder)
def target_stealer_differ(sender, instance, **kwargs):
	"""
	Datasteal / Extraction: target and stealer must be different
	"""
	if not hasattr(instance, 'target_corporation_market'):
		return

	if instance.target_corporation_market.corporation_id == instance.stealer_corporation_id:
		raise OrderNotAvailable("La cible et le bénéficiaire doivent être différents !")


@receiver(validate_order)
@sender_instance_of(DataStealOrder, ExtractionOrder)
def both_have_target_corporation_market(sender, instance, **kwargs):
	"""
	Datasteal / Extraction: The stealer must have assets on the target market
	"""

	if instance.target_corporation_market.market.name not in instance.stealer_corporation.base_corporation.markets.keys():
		raise ValidationError("Target market %s is absent from stealer corporation." % instance.target_corporation_market.market.name)


@receiver(validate_order)
@sender_instance_of(DataStealOrder, ExtractionOrder)
def target_above_stealer(sender, instance, **kwargs):
	"""
	The target in a datasteal must have more assets than the stealer on the target market
	"""

	target_value = instance.target_corporation_market.value
	stealer_value = instance.stealer_corporation_market.value

	if target_value < stealer_value:
		raise ValidationError("Target market is below the stealer on this market")
