from django.dispatch import receiver

from engine.dispatchs import post_create
from engine_modules.corporation.models import Corporation
from engine_modules.derivative.models import Derivative


@receiver(post_create, sender=Corporation)
def create_derivatives(sender, instance, **kwargs):
	if instance.base_corporation.derivative is not None:
		d, _ = Derivative.objects.get_or_create(name=instance.base_corporation.derivative, game=instance.game)
		d.corporations.add(instance)
