from django.db import models


class Share(models.Model):
	"""
	A share held by some player
	"""
	corporation = models.ForeignKey(Corporation)
	player = models.ForeignKey(Player)
	turn = models.PositiveSmallIntegerField()
