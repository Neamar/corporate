# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver
from engine.exceptions import OrderNotAvailable

from engine_modules.player_run.models import InformationRunOrder


@receiver(pre_save, sender=InformationRunOrder)
def check_target_is_not_self(sender, instance, **kwargs):
	"""
	Check if the target isn't the Johnson
	"""
	if instance.player == instance.target:
		raise OrderNotAvailable("Impossible de se cibler soi-même.")