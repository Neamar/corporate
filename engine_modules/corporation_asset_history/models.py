from django.db import models
from engine_modules.corporation.models import Corporation


class AssetHistory(models.Model):
	class Meta:
		unique_together = (("corporation","turn"),)

	corporation = models.ForeignKey(Corporation)
	assets = models.PositiveSmallIntegerField()
	turn = models.PositiveSmallIntegerField()


