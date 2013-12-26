from django.db import models
from datetime import datetime
from config.lib.models import NamedModel
from django.contrib.auth.models import User


class Game(models.Model):
	current_turn = models.PositiveIntegerField(default=1)
	total_turn = models.PositiveIntegerField()
	started = DateTimeField(default=datetime.now)

class Player(NamedModel):
	user = models.ForeignKey(User)
	game = models.ForeignKey(Game)


class Message(models.Model):
	title = models.CharField(max_length=256)
	content = models.TextField(blank=True)
	author = models.ForeignKey(Player)
	public = models.BooleanField(default=False)
	recipient_set = ManyToManyField('Player')

class Order(models.Model):
	player = models.ForeignKey(Player)
	turn = models.PositiveIntegerField()
