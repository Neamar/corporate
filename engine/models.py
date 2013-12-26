from django.db import models
from config.lib.models import NamedModel
from django.contrib.auth.models import User


class Game(models.Model):
	current_turn = models.PositiveIntegerField(default=1)
	total_turn = models.PositiveIntegerField()


class Player(NamedModel):
	user = models.OneToManyField(User)
	game = models.ForeignKey(Game)


class Message(models.Model):
	title = models.CharField(max_length=256, blank=True)
	content = models.TextField(blank=True)
	author = models.Foreignkey(Player)
	public = models.BooleanField(default=False)
	recipient = ManyToManyField('Player')

class Order(models.Model):
	player = models.Foreignkey(Player)
	game = models.ForeignKey(Game)
	turn = models.PositiveIntegerField()
