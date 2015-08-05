# -*- coding: utf-8 -*-

from django.db import models

from engine.models import Game


class Market(models.Model):
	class Meta:
		unique_together = (("game", "name"),)

	game = models.ForeignKey(Game)
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name.capitalize()


class CorporationMarket(models.Model):
	"""
	The market entry for a Corporation
	"""
	class Meta:
		ordering = ['corporation', 'market']

	corporation = models.ForeignKey("corporation.Corporation")
	market = models.ForeignKey(Market)
	# At the end of turn n, the CorporationMarket object with turn n has the values at end of turn,
	# whereas the one with turn n-1 has the values at beginning of turn.
	# This is why we have default turn 0 and we need to initialize both for turn 0 and 1
	turn = models.PositiveSmallIntegerField(default=0)
	# The meaning of 'value' and 'bubble_value' changed: value is now the market assets + the bubble modifier.
	# bubble_value is only here as a token for the bubble: 0 -> no bubble, 1 -> domination, -1 -> 'dry' bubble
	# This should greatly simplify the DB requests for the CorporationMarkets that have a bubble
	value = models.SmallIntegerField()
	# bubble_value should only be modified through the update_bubble() method
	bubble_value = models.SmallIntegerField(default=0)

	def update_bubble(self, value):
		"""
		update the bubble_value field and keep the value field consistent
		"""
		self.value += (value - self.bubble_value)
		self.bubble_value = value

	def __unicode__(self):
		return u"%s de %s" % (self.market, self.corporation)
