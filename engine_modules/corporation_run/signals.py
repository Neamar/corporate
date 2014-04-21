# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable

from engine_modules.corporation_run.models import DataStealOrder, ExtractionOrder


@receiver(validate_order, sender=DataStealOrder)
def datasteal_target_stealer_differ(sender, instance, **kwargs):
	"""
	Datasteal target and stealer must be different
	"""
	if not hasattr(instance, 'target_corporation'):
		return

	if instance.target_corporation == instance.stealer_corporation:
		raise OrderNotAvailable("La cible et le bénéficiaire doivent être différents !")


@receiver(validate_order, sender=ExtractionOrder)
def extraction_target_stealer_differ(sender, instance, **kwargs):
	"""
	Extraction target and kidnapper must be different
	"""
	if not hasattr(instance, 'target_corporation'):
		return

	if instance.target_corporation == instance.kidnapper_corporation:
		raise OrderNotAvailable("La cible et le bénéficiaire doivent être différents !")
