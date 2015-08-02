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
	# default turn is 0, because the CorporationMarket on turn n represent the status on the 
	# beginning of turn n + 1
	turn = models.PositiveSmallIntegerField(default=0)
	value = models.SmallIntegerField()

	def __unicode__(self):
		return u"%s de %s" % (self.market, self.corporation)
