from django.db import models
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory
from engine.models import Game
from django.db.models import Sum


class Derivative(models.Model):
	name = models.CharField(max_length=30)
	game = models.ForeignKey(Game)
	corporations = models.ManyToManyField(Corporation)

	def __unicode__(self):
		return self.name

	def get_sum(self, turn):
		return AssetHistory.objects.filter(corporation__in=self.corporations.all(), turn=turn).aggregate(Sum('assets'))['assets__sum']
