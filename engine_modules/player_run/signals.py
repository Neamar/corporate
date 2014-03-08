# -*- coding: utf-8 -*-
from django.dispatch import receiver
from engine.exceptions import OrderNotAvailable

from engine.dispatchs import validate_order
from engine_modules.player_run.models import InformationOrder


@receiver(validate_order, sender=InformationOrder)
def check_target_is_not_self(sender, instance, **kwargs):
	"""
	Check if the target isn't the Johnson
	"""
	if instance.target_id is not None and instance.player_id == instance.target_id:
		raise OrderNotAvailable("Impossible de se cibler soi-même.")
