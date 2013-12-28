from django.db import models

from engine.models import Game, Player


class BaseCorporation(models.Model):
	"""
	Basic corporation definition, reused for each game
	"""
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField()


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

# TODO: move dat.
def get_ordered_corporations(self):
	return list(self.corporation_set.order_by('-assets'))
Game.get_ordered_corporations = get_ordered_corporations
