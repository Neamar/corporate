from django.db import models
from engine.models import Player, Order


class PlayerInfluence(models.Model):
	player = models.OneToOneField(Player)
	level = models.PositiveSmallIntegerField()


class BuyInfluenceOrder(Order):
	pass

from engine_modules.influence.tasks import *
