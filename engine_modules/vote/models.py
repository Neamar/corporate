# -*- coding: utf-8 -*-
from django.db import models

from engine.models import Order
from engine_modules.corporation.models import Corporation
from engine_modules.market.models import Market


class VoteOrder(Order):
	"""
	Order to vote for a Corporation
	"""
	title = "Voter"
	ORDER = 0

	corporation_up = models.ForeignKey(Corporation, related_name="+")
	market_up = models.ForeignKey(Market, related_name="+")
	corporation_down = models.ForeignKey(Corporation, related_name="+")
	market_down = models.ForeignKey(Market, related_name="+")

	def resolve(self):
		self.corporation_up.update_assets(1, market=self.market_up)

		self.corporation_down.update_assets(-1, market=self.market_down)

		# Send a note for final message
		content = u"Vous avez voté pour avantager le marché %s de %s au détriment du marché %s de %s." % (self.market_up.name, self.corporation_up.base_corporation.name, self.market_down.name, self.corporation_down.base_corporation.name)
		self.player.add_note(content=content)

	def description(self):
		return u"Voter pour l'augmentation des actifs du marché %s de %s et la diminution du marché %s de %s" % (self.market_up.name, self.corporation_up.base_corporation.name, self.market_down.name, self.corporation_down.base_corporation.name)

	def get_form(self, data=None):
		form = super(VoteOrder, self).get_form(data)
		form.fields['corporation_up'].queryset = self.player.game.corporation_set.all()
		form.fields['corporation_down'].queryset = self.player.game.corporation_set.all()

		return form

orders = (VoteOrder,)
