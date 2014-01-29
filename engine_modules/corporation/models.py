from django.db import models

from engine.models import Game


class BaseCorporation(models.Model):
	"""
	Basic corporation definition, reused for each game
	"""
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField()
	initials_assets = models.PositiveSmallIntegerField(default=10)


class Corporation(models.Model):
	"""
	A corporation being part of a game
	"""
	class Meta:
		unique_together = (('base_corporation', 'game'), )

	base_corporation = models.ForeignKey(BaseCorporation)
	game = models.ForeignKey(Game)
	assets = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return "%s (%s)" % (self.base_corporation.name, self.game)
