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
		"""
		# We have to reload the corporation_market to have the object un to date
		corporation_market = CorporationMarket.objects.get(pk=self.pk)

		previous_bubble_value = corporation_market.bubble_value
		# We save the bubble value on the corporation market bubble_value field with no impact on the value field
		corporation_market.bubble_value = value
		corporation_market.save()

		delta = value - previous_bubble_value

		# On ajoute la bulle sur les actifs de la corpo
		self.corporation.update_modifier(delta)
		return delta

	def __unicode__(self):
		return u"%s , marché %s (%s)" % (self.corporation.base_corporation.name, self.market.name, self.value)
