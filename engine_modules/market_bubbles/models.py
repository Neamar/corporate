# -*- coding: utf-8 -*-
from django.db import models

from engine_modules.market.models import Market
from engine_modules.corporation.models import Corporation


class MarketBubble(models.Model):
	"""
	A market bubble represents the domination of a corporation or its defeat in a specifc market.
	It gives a bonus or a malus of one asset (which can bring the assets into the negatives).
	"""
	class Meta:
		unique_together = (("corporation", "market", "turn"),)

	corporation = models.ForeignKey(Corporation, related_name='market_bubbles', null=True, default=None)
	market = models.ForeignKey(Market, related_name='bubbles')
	turn = models.PositiveSmallIntegerField()
	value = models.SmallIntegerField()

	def __unicode__(self):
		return u"%s (%i) in %s" % (self.corporation, self.value, self.market)
