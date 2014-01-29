from django.db import models
from engine_modules.corporation.models import Corporation
from engine.models import Game
from collections import defaultdict


class AssetHistory(models.Model):
	"""
	Store corporation assets, turn by turn
	"""

	class Meta:
		unique_together = (("corporation","turn"),)

	corporation = models.ForeignKey(Corporation)
	assets = models.PositiveSmallIntegerField()
	turn = models.PositiveSmallIntegerField()


def get_ordered_corporations(self):
	Previous = AssetHistory.objects.filter(corporation__game=self)
	ranking = defaultdict(lambda:0)
	for element in Previous:
		ranking[element.corporation] += element.assets*10^(2*element.turn)

	Actual=Corporation.objects.filter(game=self)
	for element in Actual:
		ranking[element] += element.assets*10^(2*self.current_turn)

	Ordered_corporation=sorted(ranking, key=lambda c:ranking[c], reverse=True)
	return Ordered_corporation
Game.get_ordered_corporations = get_ordered_corporations


