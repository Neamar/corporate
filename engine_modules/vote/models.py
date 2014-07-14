# -*- coding: utf-8 -*-
from django.db import models

from engine.models import Order
from engine_modules.market.models import CorporationMarket
from messaging.models import Newsfeed


class VoteOrder(Order):
	"""
	Order to vote for a Corporation market and increase or decrease it
	"""
	title = "Voter"
	ORDER = 0

	corporation_market_up = models.ForeignKey(CorporationMarket, related_name="+")
	corporation_market_down = models.ForeignKey(CorporationMarket, related_name="+")

	def resolve(self):
		self.corporation_market_up.corporation.update_assets(1, market=self.corporation_market_up.market)
		self.corporation_market_down.corporation.update_assets(-1, market=self.corporation_market_down.market)

		# Send a note for final message
		content = u"Vous avez voté pour avantager le marché %s de %s au détriment du marché %s de %s." % (self.corporation_market_up.market, self.corporation_market_up.corporation.base_corporation.name, self.corporation_market_down.market, self.corporation_market_down.corporation.base_corporation.name)
		self.player.add_note(content=content)

		# Create the newsfeed
		content = u"%s a voté pour mettre un +1 sur le marché %s de %s." % (self.player.name, self.corporation_market_up.market.name, self.corporation_market_up.corporation.base_corporation.name)
		self.player.game.add_newsfeed(category=Newsfeed.ECONOMY, content=content, status=Newsfeed.PRIVATE, market=self.corporation_market_up.market, corporations=[self.corporation_market_up.corporation], players=[self.player])

		content = u"%s a voté pour mettre un -1 sur le marché %s de %s." % (self.player.name, self.corporation_market_down.market, self.corporation_market_down.corporation.base_corporation.name)
		self.player.game.add_newsfeed(category=Newsfeed.ECONOMY, content=content, status=Newsfeed.PRIVATE, market=self.corporation_market_down.market, corporations=[self.corporation_market_down.corporation], players=[self.player])

	def description(self):
		return u"Voter pour l'augmentation des actifs du marché %s de %s et la diminution du marché %s de %s" % (self.corporation_market_up.market, self.corporation_market_up.corporation.base_corporation.name, self.corporation_market_down.market, self.corporation_market_down.corporation.base_corporation.name)

	def get_form(self, data=None):
		form = super(VoteOrder, self).get_form(data)
		form.fields['corporation_market_up'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game)
		form.fields['corporation_market_down'].queryset = form.fields['corporation_market_up'].queryset

		return form

orders = (VoteOrder,)
