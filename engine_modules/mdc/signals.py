# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.dispatchs import validate_order, post_create
from engine.exceptions import OrderNotAvailable
from engine.decorators import sender_instance_of
from engine_modules.mdc.models import MDCVoteOrder
from engine_modules.corporation_run.models import ProtectionOrder, OffensiveRunOrder
from engine_modules.player_run.models import InformationOrder
from engine_modules.speculation.models import CorporationSpeculationOrder, DerivativeSpeculationOrder
from engine_modules.mdc.decorators import expect_party_line


@receiver(validate_order, sender=MDCVoteOrder)
def limit_mdc_order(sender, instance, **kwargs):
	"""
	Can't vote twice the same turn
	"""
	if MDCVoteOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Vous ne pouvez pas voter deux fois dans le même tour.")


@receiver(post_create)
@sender_instance_of(OffensiveRunOrder)
@expect_party_line(MDCVoteOrder.CCIB)
def enforce_mdc_ccib_positive(sender, instance, **kwargs):
	"""
	When CCIB line is active, corporation gives a 10%% malus to attackers
	"""
	g = instance.player.game
	protected_corporations = []
	right_vote_orders = MDCVoteOrder.objects.filter(player__game=g, turn=g.current_turn - 1, party_line=MDCVoteOrder.CCIB)
	for vo in right_vote_orders:
		protected_corporations += vo.get_friendly_corporations()
	if instance.target_corporation in protected_corporations:
		instance.hidden_percents -= 1


@receiver(post_create)
@sender_instance_of(OffensiveRunOrder, InformationOrder)
@expect_party_line(MDCVoteOrder.TRAN)
def enforce_mdc_tran(sender, instance, **kwargs):
	"""
	When TRAN line is active,
	* +10%% for TRAN player
	* -10%% for TRAN player
	"""
	player_vote = instance.player.get_last_mdc_vote()
	if player_vote == MDCVoteOrder.CCIB:
		instance.hidden_percents -= 1

	elif player_vote == MDCVoteOrder.TRAN:
		instance.hidden_percents += 1


@receiver(validate_order, sender=ProtectionOrder)
@expect_party_line(MDCVoteOrder.CCIB)
def enforce_mdc_ccib_negative(sender, instance, **kwargs):
	"""
	When CCIB line is active, TRAN players can't protect.
	"""
	if instance.player.get_last_mdc_vote() == MDCVoteOrder.TRAN:
		raise OrderNotAvailable("Vous avez voté pour la transparence au tour précédent, vous ne pouvez donc pas effectuer de run de protection ce tour-ci")


@receiver(validate_order)
@sender_instance_of(CorporationSpeculationOrder, DerivativeSpeculationOrder)
@expect_party_line(MDCVoteOrder.DERE)
def enforce_mdc_dere_negative(sender, instance, **kwargs):
	"""
	When DERE line is active, BANK players can't speculate
	"""
	if instance.player.get_last_mdc_vote() == MDCVoteOrder.BANK:
		raise OrderNotAvailable("Vous avez voté pour l'instauration de garde-fous bancaires au tour précédent, vous ne pouvez donc pas spéculer ce tour-ci")


@receiver(validate_order)
@sender_instance_of(CorporationSpeculationOrder, DerivativeSpeculationOrder)
@expect_party_line(MDCVoteOrder.BANK)
def enforce_mdc_bank_negative(sender, instance, **kwargs):
	"""
	When BANK line is active, DERE players can't speculate
	"""

	if instance.player.get_last_mdc_vote() == MDCVoteOrder.DERE:
		raise OrderNotAvailable("Vous avez voté pour la dérégulation au tour précédent, vous ne pouvez donc pas spéculer ce tour-ci")


@receiver(post_create)
@sender_instance_of(CorporationSpeculationOrder, DerivativeSpeculationOrder)
@expect_party_line(MDCVoteOrder.BANK)
def enforce_mdc_bank_positive(sender, instance, **kwargs):
	"""
	When BANK is active, BANK players can speculate without losing money
	"""
	if instance.player.get_last_mdc_vote() == MDCVoteOrder.BANK:
		# This speculation should cost nothing if it fails
		instance.on_loss_ratio = 0
		instance.save()


@receiver(post_create)
@sender_instance_of(CorporationSpeculationOrder, DerivativeSpeculationOrder)
@expect_party_line(MDCVoteOrder.DERE)
def enforce_mdc_dere_positive(sender, instance, **kwargs):
	"""
	When DERE is active, DERE players can speculate and gain more.
	"""
	if instance.player.get_last_mdc_vote() == MDCVoteOrder.DERE:
		# This speculation should see its rate augmented if it succeeds
		instance.on_win_ratio += 1
		instance.save()
