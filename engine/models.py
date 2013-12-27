from django.db import models
from django.conf import settings

class Game(models.Model):
	current_turn = models.PositiveIntegerField(default=1)
	total_turn = models.PositiveIntegerField()
	started = models.DateTimeField(auto_now_add=True)

class Player(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	game = models.ForeignKey(Game)
	name = models.CharField(max_length=64)

class Message(models.Model):
	title = models.CharField(max_length=256)
	content = models.TextField(blank=True)
	author = models.ForeignKey(Player)
	public = models.BooleanField(default=False)
	recipient_set = models.ManyToManyField('Player', related_name="+")

class Order(models.Model):
	player = models.ForeignKey(Player)
	turn = models.PositiveIntegerField()

from engine.signals import *