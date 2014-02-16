from django.db import models
from engine_modules.corporation.models import Corporation
from engine.models import Game
from collections import defaultdict


class AssetHistory(models.Model):
	"""
	Store corporation assets, turn by turn
	"""

	class Meta:
		unique_together = (("corporation", "turn"),)

	corporation = models.ForeignKey(Corporation)
	assets = models.PositiveSmallIntegerField()
	turn = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return "%s assets for %s on turn %s" % (self.assets, self.corporation.base_corporation.name, self.turn)


def get_ordered_corporations(self):
	"""
	order corporation by assets
	if ex-aequo order by assets the turn before and the turn even before until the turn 1
	if ex-aequo again, order by the first in the sql request. Postgres should always send them in the same order
	"""
	previous = AssetHistory.objects.filter(corporation__game=self)
	ranking = defaultdict(lambda: 0)
	for element in previous:
		ranking[element.corporation] += element.assets * pow(10 , (2 * element.turn))

	actual = Corporation.objects.filter(game=self)
	for element in actual:
		ranking[element] += element.assets * pow(10 , (2 * self.current_turn))

	ordered_corporation = sorted(ranking, key=lambda c: ranking[c], reverse=True)
	return ordered_corporation
Game.get_ordered_corporations = get_ordered_corporations
