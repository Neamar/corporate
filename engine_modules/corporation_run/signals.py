# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable

from engine_modules.corporation_run.models import DataStealOrder, ExtractionOrder
from django.core.exceptions import ValidationError

@receiver(validate_order, sender=DataStealOrder)
def datasteal_target_stealer_differ(sender, instance, **kwargs):
	"""
	Datasteal target and stealer must be different
	"""
	if not hasattr(instance, 'target_corporation'):
		return

	if instance.target_corporation == instance.stealer_corporation:
		raise OrderNotAvailable("La cible et le bénéficiaire doivent être différents !")

@receiver(validate_order, sender=DataStealOrder)
def datasteal_both_have_target_market(sender, instance, **kwargs):
	"""
	The target and the stealer in a datasteal must both have assets on the target market
	"""

	if not instance.target_market.market.name in instance.target_corporation.base_corporation.markets.keys():
		raise ValidationError("Target market is absent from target corporation.")

	if not instance.target_market.market.name in instance.stealer_corporation.base_corporation.markets.keys():
		raise ValidationError("Target market is absent from stealer corporation.")

@receiver(validate_order, sender=ExtractionOrder)
def extraction_target_stealer_differ(sender, instance, **kwargs):
	"""
	Extraction target and kidnapper must be different
	"""
	if not hasattr(instance, 'target_corporation'):
		return

	if instance.target_corporation == instance.kidnapper_corporation:
		raise OrderNotAvailable("La cible et le bénéficiaire doivent être différents !")
