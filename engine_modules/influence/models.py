from django.db import models
from engine.models import Player


class PlayerInfluence(models.model):
	player = models.OneToOneField(Player)
	level = models.PositiveSmallIntegerField()
