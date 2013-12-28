from django.db import models
from engine.models import Player
from engine_modules.corporation.models import Corporation

class CitizenShip(models.Model):
	player = models.OneToOneField(Player)
	corporation = models.ForeignKey(Corporation)