from django.db import models
from datetime import datetime
from django.conf import settings

class Game(models.Model):
	city = models.CharField(max_length=50)
	current_turn = models.PositiveSmallIntegerField(default=1)
	total_turn = models.PositiveSmallIntegerField()
	started = models.DateTimeField(default=datetime.now)

	def resolve_current_turn(self):
		"""
		Resolve all orders for this turn, increment current_turn by 1.
		"""
		pass

	def __unicode__(self):
		return "Corporate Game: %s" % self.city


class Player(models.Model):
	name = models.CharField(max_length=64)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	game = models.ForeignKey(Game)

	def get_current_orders(self):
		"""
		Returns the list of order for this turn
		"""
		return self.order_set.filter(turn=self.game.current_turn)

	def __unicode__(self):
		return self.name


class Message(models.Model):
	title = models.CharField(max_length=256)
	content = models.TextField(blank=True)
	author = models.ForeignKey(Player)
	public = models.BooleanField(default=False)
	recipient_set = models.ManyToManyField('Player', related_name="+")


class Order(models.Model):
	player = models.ForeignKey(Player)
	turn = models.PositiveSmallIntegerField(blank=True)
	type = models.CharField(max_length=50, blank=True, editable=False)

	def save(self):
		# Save the current type to inflate later
		if self.__class__.__name__ == "Order":
			raise Exception("You can't save raw Order, only subclasses")

		self.type = self.__class__.__name__

		# Turn default values is game current_turn
		if not self.turn:
			self.turn = self.player.game.current_turn

		super(Order, self).save()

	def __unicode__(self):
		return "%s for %s, turn %s" % (self.type, self.player, self.turn)


from engine.modules import *
