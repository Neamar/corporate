# -*- coding: utf-8 -*-
from django.db import models

from engine.models import Order, Game
from engine_modules.market.models import CorporationMarket


class VoteOrder(Order):
	"""
	Order to vote for a Corporation market and increase or decrease it
	"""
	title = "Voix au chapitre"
	ORDER = 0

	corporation_market_up = models.ForeignKey(CorporationMarket, related_name="+")
	corporation_market_down = models.ForeignKey(CorporationMarket, related_name="+")

	def resolve(self):
		# apply the effect voice up
		self.corporation_market_up.corporation.update_assets(1, corporation_market=self.corporation_market_up)
		# Create the game event
		self.corporation_market_up.corporation.game.add_event(event_type=Game.VOICE_UP, data={"player": self.player.name, "corporation": self.corporation_market_up.corporation.base_corporation.name, "market": self.corporation_market_up.market.name}, delta=1, corporation=self.corporation_market_up.corporation, corporation_market=self.corporation_market_up, players=[self.player])

		# apply the effect voice down
		self.corporation_market_down.corporation.update_assets(-1, corporation_market=self.corporation_market_down)
		# Create the game event
		self.corporation_market_up.corporation.game.add_event(event_type=Game.VOICE_DOWN, data={"player": self.player.name, "corporation": self.corporation_market_down.corporation.base_corporation.name, "market": self.corporation_market_down.market.name}, delta=-1, corporation=self.corporation_market_down.corporation, corporation_market=self.corporation_market_down, players=[self.player])

	def description(self):
		return u"Voter pour l'augmentation des actifs du marché %s de %s et la diminution du marché %s de %s" % (self.corporation_market_up.market, self.corporation_market_up.corporation.base_corporation.name, self.corporation_market_down.market, self.corporation_market_down.corporation.base_corporation.name)

	def get_form(self, data=None):
		form = super(VoteOrder, self).get_form(data)
		form.fields['corporation_market_up'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game, corporation__crash_turn__isnull=True, turn=self.player.game.current_turn).select_related('market', 'corporation')
		form.fields['corporation_market_down'].queryset = form.fields['corporation_market_up'].queryset.filter(value__gte=0)
		form.fields['corporation_market_up'].label = u'Positif'
		form.fields['corporation_market_down'].label = u'Negatif'

		return form

orders = (VoteOrder,)
