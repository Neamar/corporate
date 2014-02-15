# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order
from engine.models import Order
from engine.exceptions import OrderNotAvailable
from engine_modules.mdc.models import MDCVoteOrder
from engine_modules.corporation_run.models import ProtectionOrder, SabotageOrder, DataStealOrder, OffensiveRunOrder
from engine_modules.player_run.models import InformationRunOrder
from engine_modules.speculation.models import CorporationSpeculationOrder, DerivativeSpeculationOrder


@receiver(validate_order, sender=ProtectionOrder)
def enforce_mdc_party_line_protection(sender, instance, **kwargs):

	party_line = instance.player.game.get_current_mdc_party_line()

	if party_line == MDCVoteOrder.CCIB:
		if instance.player.get_last_mdc_vote() == MDCVoteOrder.TRAN:
			instance.hidden_percents = -1

@receiver(validate_order)
def enforce_mdc_party_line_offense(instance, **kwargs):

	if not (isinstance(instance, InformationRunOrder) or isinstance(instance, OffensiveRunOrder)):
		return

	party_line = instance.player.game.get_current_mdc_party_line()

	if party_line == MDCVoteOrder.TRAN:
		if instance.player.get_last_mdc_vote() == MDCVoteOrder.CCIB:
			instance.hidden_percents = -1
		
		elif instance.player.get_last_mdc_vote() == MDCVoteOrder.TRAN:
			instance.hidden_percents = 1

@receiver(validate_order)
def enforce_mdc_party_line_no_speculation(instance, **kwargs):

	if not (isinstance(instance, CorporationSpeculationOrder) or isinstance(instance, DerivativeSpeculationOrder)):
		return

	party_line = instance.player.game.get_current_mdc_party_line()

	if party_line == MDCVoteOrder.BANK:
		if instance.player.get_last_mdc_vote() == MDCVoteOrder.DERE:
			raise OrderNotAvailable("Vous avez voté pour la dérégulation au tour précédent, vous ne pouvez donc pas spéculer ce tour-ci")

	elif party_line == MDCVoteOrder.DERE:
		if instance.player.get_last_mdc_vote() == MDCVoteOrder.BANK:
                        raise OrderNotAvailable("Vous avez voté pour l'instauration de garde-fous bancaires au tour précédent, vous ne pouvez donc pas spéculer ce tour-ci")

