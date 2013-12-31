from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from engine.dispatchs import validate_order


class Game(models.Model):
	city = models.CharField(max_length=50)
	current_turn = models.PositiveSmallIntegerField(default=1)
	total_turn = models.PositiveSmallIntegerField()
	started = models.DateTimeField(auto_now_add=True)

	def resolve_current_turn(self):
		"""
		Resolve all orders for this turn, increment current_turn by 1.
		"""
		from engine.modules import tasks_list
		for task in tasks_list:
			t = task()
			t.run(self)

		self.current_turn += 1
		self.save()

	def __unicode__(self):
		return "Corporate Game: %s" % self.city


class Player(models.Model):
	class Meta:
		unique_together = (("game", "user"),)

	name = models.CharField(max_length=64)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	game = models.ForeignKey(Game)
	money = models.PositiveIntegerField(default=0)

	def get_current_orders(self):
		"""
		Returns the list of order for this turn
		"""
		return self.order_set.filter(turn=self.game.current_turn)

	def get_current_orders_cost(self):
		return sum([order.cost for order in self.get_current_orders()])

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
	turn = models.PositiveSmallIntegerField(editable=False)
	cost = models.PositiveSmallIntegerField(editable=False)
	type = models.CharField(max_length=80, blank=True, editable=False)

	def save(self):
		# Save the current type to inflate later
		self.type = '%s.%s' % (self._meta.app_label, self._meta.object_name)
		# Turn default values is game current_turn
		if not self.turn:
			self.turn = self.player.game.current_turn

		if not self.cost:
			self.cost = self.get_cost()


		super(Order, self).save()

	def clean(self):
		if self.__class__.__name__ == "Order":
			raise ValidationError("You can't save raw Order, only subclasses")
		validate_order.send(sender=self.__class__, instance=self)

	def resolve(self):
		raise NotImplementedError("Abstract call.")

	def get_cost(self):
		return 0

	def __unicode__(self):
		return "%s for %s, turn %s" % (self.type, self.player, self.turn)


# Import datas for all engine_modules
from engine.modules import *

# Import signals
from engine.signals import *
