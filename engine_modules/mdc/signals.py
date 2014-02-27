# -*- coding: utf-8 -*-
from django.dispatch import receiver
from engine.dispatchs import validate_order
from engine.models import Order
from engine.exceptions import OrderNotAvailable
from engine_modules.mdc.models import MDCVoteOrder
from engine_modules.corporation_run.models import ProtectionOrder, SabotageOrder, DataStealOrder, OffensiveRunOrder
from engine_modules.player_run.models import InformationOrder
from engine_modules.speculation.models import CorporationSpeculationOrder, DerivativeSpeculationOrder



@receiver(validate_order)
def enforce_mdc_party_line_offense(instance, **kwargs):

	if not (isinstance(instance, InformationOrder) or isinstance(instance, OffensiveRunOrder)):
		return

	party_line = instance.player.game.get_current_mdc_party_line()
	player_vote = instance.player.get_last_mdc_vote()

	if isinstance(instance, OffensiveRunOrder):
		if party_line == MDCVoteOrder.CCIB:
			g =instance.player.game
			protected_corporations = []
			# This call is going to be a DataBase catastrophe !!!!
			right_vote_orders = MDCVoteOrder.objects.filter(player__game=g, turn=g.current_turn - 1, party_line=MDCVoteOrder.CCIB)
			for vo in right_vote_orders:
				protected_corporations += vo.get_friendly_corporations()
			
			if instance.target_corporation.base_corporation_slug in protected_corporations:
				instance.hidden_percents -= 1

	if party_line == MDCVoteOrder.TRAN:
		if player_vote == MDCVoteOrder.CCIB:
			instance.hidden_percents -= 1
		
		elif player_vote == MDCVoteOrder.TRAN:
			instance.hidden_percents += 1

@receiver(validate_order, sender=ProtectionOrder)
def enforce_mdc_party_line_no_protection(sender, instance, **kwargs):

	party_line = instance.player.game.get_current_mdc_party_line()

	if party_line == MDCVoteOrder.CCIB:
		if instance.player.get_last_mdc_vote() == MDCVoteOrder.TRAN:
			raise OrderNotAvailable("Vous avez voté pour la transparence au tour précédent, vous ne pouvez donc pas effectuer de run de protection ce tour-ci")

@receiver(validate_order)
def enforce_mdc_party_line_no_speculation(instance, **kwargs):

	if not (isinstance(instance, CorporationSpeculationOrder) or isinstance(instance, DerivativeSpeculationOrder)):
		return

	party_line = instance.player.game.get_current_mdc_party_line()
	player_vote = instance.player.get_last_mdc_vote()

	if party_line == MDCVoteOrder.BANK:
		if player_vote == MDCVoteOrder.DERE:
			raise OrderNotAvailable("Vous avez voté pour la dérégulation au tour précédent, vous ne pouvez donc pas spéculer ce tour-ci")

	elif party_line == MDCVoteOrder.DERE:
		if player_vote == MDCVoteOrder.BANK:
                        raise OrderNotAvailable("Vous avez voté pour l'instauration de garde-fous bancaires au tour précédent, vous ne pouvez donc pas spéculer ce tour-ci")

@receiver(validate_order)
def enforce_mdc_party_line_speculation_rates(instance, **kwargs):

	if not (isinstance(instance, CorporationSpeculationOrder) or isinstance(instance, DerivativeSpeculationOrder)):
		return

	party_line = instance.player.game.get_current_mdc_party_line()
	player_vote = instance.player.get_last_mdc_vote()

	if party_line == MDCVoteOrder.BANK:
		if player_vote == MDCVoteOrder.BANK:
			# This speculation should cost nothing if it fails
			instance.set_lossrate(0)

	if party_line == MDCVoteOrder.DERE:
		if player_vote == MDCVoteOrder.DERE:
			# This speculation should see its rate augmented if it succeeds
			instance.set_winrate(instance.winrate + 1)

@receiver(validate_order, sender=MDCVoteOrder)
def limit_mdc_order(sender, instance, **kwargs):
	"""
	Can't vote twice the same turn
	"""
	if MDCVoteOrder.objects.filter(player=instance.player, turn=instance.player.game.current_turn).exists():
		raise OrderNotAvailable("Vous ne pouvez pas voter deux fois dans le même tour.")
