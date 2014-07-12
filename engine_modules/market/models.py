# -*- coding: utf-8 -*-

from django.db import models

from engine.models import Game


class Market(models.Model):
	game = models.ForeignKey(Game)
	name = models.CharField(max_length=20)


class CorporationMarket(models.Model):
	"""
	The market entry for a Corporation
	"""

	corporation = models.ForeignKey("corporation.Corporation")
	market = models.ForeignKey(Market)
	value = models.SmallIntegerField()
