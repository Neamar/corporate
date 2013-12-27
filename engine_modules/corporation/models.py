from django.db import models

from engine.models import Game


class BaseCorporation(models.Model):
	"""
	Basic corporation definition, reused for each game
	"""
	name = models.CharField(max_length=50)
	description = models.TextField()


class Corporation(models.Model):
	"""
	A corporation being part of a game
	"""
	
	base_corporation = models.ForeignKey(BaseCorporation)
	game = models.ForeignKey(Game)
	assets = models.PositiveSmallIntegerField()
