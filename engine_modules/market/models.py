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
	# @Neamar: We explain in the method update_assets of the Corporation Class that a market value
	# can't be negative, so shouldn't this be:
	# value = models.PositiveSmallIntegerField()
	value = models.SmallIntegerField()

	def __unicode__(self):
		return "%s de %s" % (self.market, self.corporation)
