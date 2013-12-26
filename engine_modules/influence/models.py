from django.db import models
from engine.models import Player


class Influence(models.Model):
	player = models.OneToOneField(Player)
	level = models.PositiveSmallIntegerField()
