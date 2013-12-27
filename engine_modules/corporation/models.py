from django.db import models

from engine.models import Game


class BaseCorporation(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()


class Corporation(models.Model):
	base_corporation = models.ForeignKey(BaseCorporation)
	game = models.ForeignKey(Game)
	assets = models.PositiveSmallIntegerField()
