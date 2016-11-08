# -*- coding: utf-8 -*-
from django.db import models
from django import forms

from engine.models import Player, Order, Game
from engine_modules.corporation.models import Corporation


class PlayerPoints(models.Model):
	"""
	Class for holding the player's points
	"""

	player = models.ForeignKey(Player)
	turn = models.PositiveSmallIntegerField(default=0)

	# These are the categories of points defined in the rules
	total_points = models.SmallIntegerField(default=0)
	share_points = models.SmallIntegerField(default=0)
	citizenship_points = models.SmallIntegerField(default=0)
	background_points = models.SmallIntegerField(default=0)
