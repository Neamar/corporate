# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from engine_modules.corporation.models import Corporation

class CorporationMarket(models.Model):
	"""
	The market entry for a Corporation
	"""

	corporation = models.ForeignKey(Corporation)
	name = models.CharField(max_length=20)
	value = models.SmallIntegerField()
