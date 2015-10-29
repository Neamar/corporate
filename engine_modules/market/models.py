# -*- coding: utf-8 -*-

from django.db import models

from engine.models import Game
from engine_modules.corporation.models import AssetDelta


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

	DOMINATION_BUBBLE = 1
	NO_BUBBLE = 0
	NEGATIVE_BUBBLE = -1
	BUBBLE_VALUES = (
		(DOMINATION_BUBBLE, 'Bulle de domination'),
		(NO_BUBBLE, 'Pas de bulle'),
		(NEGATIVE_BUBBLE, 'Bulle négative')
	)
	corporation = models.ForeignKey("corporation.Corporation")
	market = models.ForeignKey(Market)
	# At the end of turn n, the CorporationMarket object with turn n has the values at end of turn,
	# whereas the one with turn n-1 has the values at beginning of turn.
	# This is why we have default turn 0 and we need to initialize both for turn 0 and 1
	turn = models.PositiveSmallIntegerField(default=0)
	# value is the market assets + the bubble modifier.
	value = models.SmallIntegerField()
	# bubble_value is only here as a token for the bubble: 0 -> no bubble, 1 -> domination, -1 -> 'dry' bubble
	# bubble_value should only be modified through the update_bubble() method
	bubble_value = models.SmallIntegerField(choices=BUBBLE_VALUES, default=NO_BUBBLE)

	def update_bubble(self, value):
		"""
		update the bubble_value field and keep the value field consistent
		We'll internalize some of the considerations when you cross the 0 threshold in a direction or the other
		Because of that, we have to return the amount by which self.bubble_value actually changed, which may be different from the amount requested
		"""

		previous_bubble_value = self.bubble_value
		# We have to specially handle the case where the resulting value would be 0
		self.value += (value - self.bubble_value)
		# You can't go into negative values unless you have a negative bubble
		if value > -1:
			self.value = max(self.value, 0)
		self.bubble_value = value
		if self.value == 0 and previous_bubble_value != 0:
			self.value -= 1
			self.bubble_value -= 1
		self.save()

		delta = self.bubble_value - previous_bubble_value
		self.corporation.assetdelta_set.create(category=AssetDelta.BUBBLE, delta=delta, turn=self.turn)
		return delta

	def __unicode__(self):
		return u"%s , marché %s (tour %s)" % (self.corporation.base_corporation.name, self.market.name, self.corporation.game.current_turn)
