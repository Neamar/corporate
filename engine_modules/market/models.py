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
	value = models.SmallIntegerField()

	def __unicode__(self):
		return u"%s de %s (tour %s)" % (self.market, self.corporation, self.corporation.game.current_turn)
