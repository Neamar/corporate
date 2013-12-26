from django.db import models
from engine.models import Player


class PlayerInfluence(models.Model):
	player = models.OneToOneField(Player)
	level = models.PositiveSmallIntegerField()


from engine_modules.influence.orders import *
from engine_modules.influence.tasks import *
