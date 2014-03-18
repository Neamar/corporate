# -*- coding: utf-8 -*-
from django.dispatch import receiver
from engine.exceptions import OrderNotAvailable

from engine.dispatchs import validate_order
from engine_modules.wiretransfer.models import WiretransferOrder


@receiver(validate_order, sender=WiretransferOrder)
def check_recipient_is_not_self(sender, instance, **kwargs):
	"""
	Check if the recipient isn't the sender
	"""
	if instance.recipient_id is not None and instance.player_id == instance.recipient_id:
		raise OrderNotAvailable("Impossible de s'envoyer de l'argent !")
