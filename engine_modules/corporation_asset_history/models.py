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
	assets = models.SmallIntegerField()
	turn = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return u"%s assets for %s on turn %s" % (self.assets, self.corporation.base_corporation.name, self.turn)


def get_ladder(self, turn=None):
	"""
	Order corporation in a game by assets
	If ex-aequo order by assets the turn before and the turn even before until turn 1
	If ex-aequo again, order by the first in the sql request. DB should always send them in the same order
	May cause sporadical error if we have several nodes in database engine though
	"""
	if turn is None:
		turn = self.current_turn + 1

	previous = AssetHistory.objects.filter(corporation__game=self, turn__lte=turn).exclude(corporation__crash_turn__lte=turn - 1).select_related('corporation')
	ranking = defaultdict(lambda: 0)
	for element in previous:
		ranking[element.corporation] += element.assets * pow(10, 2 * element.turn)

	# We're asking for a ladder on a turn where the AssetHistory have not been written yet.
	if turn > self.current_turn:
		actual = self.corporation_set.exclude(crash_turn__lte=turn)
		for element in actual:
			ranking[element] += element.assets * pow(10, 2 * self.current_turn)

	ordered_corporation = sorted(ranking, key=lambda c: ranking[c], reverse=True)
	return ordered_corporation
Game.get_ladder = get_ladder
