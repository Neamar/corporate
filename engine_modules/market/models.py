# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from engine.models import Game
from engine_modules.corporation.models import Corporation

class Market(models.Model):
	game = models.ForeignKey(Game)
	name = models.CharField(max_length=20)

class CorporationMarket(models.Model):
	"""
	The market entry for a Corporation
	"""

	corporation = models.ForeignKey(Corporation)
	market = models.ForeignKey(Market)
	value = models.SmallIntegerField()
