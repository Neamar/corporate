# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from engine.decorators import sender_instance_of
from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable
from engine_modules.run.models import RunOrder
from engine_modules.corporation_run.models import CorporationRunOrder, CorporationRunOrderWithStealer, ProtectionOrder


@receiver(validate_order)
@sender_instance_of(ProtectionOrder)
def protected_market_positive(sender, instance, **kwargs):
	"""
	Protected market must be strictly positive
	"""
	if not hasattr(instance, 'protected_corporation_market'):
		return

	if instance.protected_corporation_market.value < 0:
		raise OrderNotAvailable(u"Le marché «%s»est déjà dans le négatif pour la corpo %s, il est inutile de le protéger.")


@receiver(validate_order)
@sender_instance_of(CorporationRunOrder)
def target_market_positive(sender, instance, **kwargs):
	"""
	Target market must be strictly positive
	"""
	if not hasattr(instance, 'target_corporation_market'):
		return

	if instance.target_corporation_market.value < 0:
		raise OrderNotAvailable(u"Le marché «%s» est déjà dans le négatif pour la corpo %s, il ne lui reste que des dettes.")


@receiver(validate_order)
@sender_instance_of(CorporationRunOrder)
def target_market_unique(sender, instance, **kwargs):
	"""
	Only one run is allowed by target
	"""
	if hasattr(instance.player.game, 'allow_several_runs_on_one_target'):
		if instance.player.game.allow_several_runs_on_one_target:
			return

	if not hasattr(instance, 'target_corporation_market'):
		return
	if RunOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn, corporationrunorder__target_corporation_market=instance.target_corporation_market).count() > 0:
		raise OrderNotAvailable(u"Vous avez déjà une opération en cours sur le même marché et la même corporation.")


@receiver(validate_order)
@sender_instance_of(CorporationRunOrderWithStealer)
def target_stealer_differ(sender, instance, **kwargs):
	"""
	Datasteal / Extraction: target and stealer must be different
	"""
	if not hasattr(instance, 'target_corporation'):
		return
	if not hasattr(instance, 'stealer_corporation'):
		return

	if instance.target_corporation == instance.stealer_corporation:
		raise OrderNotAvailable(u"La cible et le bénéficiaire doivent être différents !")


@receiver(validate_order)
@sender_instance_of(CorporationRunOrderWithStealer)
def both_have_target_corporation_market(sender, instance, **kwargs):
	"""
	Datasteal / Extraction: The stealer must have assets on the target market
	"""

	if not hasattr(instance, 'target_corporation_market'):
		return

	if instance.target_corporation_market.market.name not in instance.stealer_corporation.base_corporation.markets.keys():
		raise ValidationError(u"Le marché « %s » n'est pas présent sur %s." % (instance.target_corporation_market.market.name, instance.stealer_corporation.base_corporation.name))


@receiver(validate_order)
@sender_instance_of(CorporationRunOrderWithStealer)
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
