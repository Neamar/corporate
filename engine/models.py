from django.db import models
from config.lib.models import NamedModel
from django.contrib.auth.models import User


class Game(models.Model):
	current_turn = models.PositiveIntegerField(default=1)
	total_turn = models.PositiveIntegerField(default=1)


class Player(NamedModel):
	user = models.OneToOneField(User, null=True)
	game = models.ForeignKey(Game, null=True)


class Message(models.Model):
	title = models.CharField(max_length=256, blank=True)
	content = models.TextField(blank=True)
	author = models.Foreignkey(Player, null=True)
	public = models.BooleanField(default=False)


class Order(models.Model):
	player = models.Foreignkey(Player, null=True)
	game = models.ForeignKey(Game, null=True)
	turn = models.PositiveIntegerField(default=1)
