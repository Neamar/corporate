# -*- coding: utf-8 -*-
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

		# First step: build a message containing order list.
		for player in self.player_set.all():
			player.build_order_message()

		from engine.modules import tasks_list
		for task in tasks_list:
			t = task()
			t.run(self)

		self.build_global_resolution_message()
		self.current_turn += 1
		self.save()

	def build_global_resolution_message(self):
		"""
		Build the message to sent to all the players.
		"""
		messages = Message.objects.filter(flag=Message.GLOBAL_NOTE).order_by('title')
		resolution_message = u"### Résolution du tour %s ###" % self.current_turn
		past_title=""
		for message in messages:
			current_title=message.title
			if current_title==past_title:
				resolution_message += u"%s\n" % message.content
			else:
				resolution_message += u"\n[b]%s[/b]\n%s\n" % (message.title, message.content) #Change Bold title if this isn't right
			past_title=current_title
		m=Message.objects.create(
			title="Informations publiques du tour %s" % self.current_turn,
			content=resolution_message,
			author=None,
			flag=Message.GLOBAL_RESOLUTION)
		m.save()
		for player in Player.objects.filter(game=self):
		  m.recipient_set.add(player)
		return m

	def add_global_note(self, **kwargs):
		"""
		Create a note for the global resolution message
		"""
		m = Message.objects.create(flag=Message.GLOBAL_NOTE, author=None, **kwargs)
		m.save()
		return m

	def __unicode__(self):
		return "Corporate Game: %s" % self.city


class Player(models.Model):
	class Meta:
		unique_together = (("game", "user"),)

	name = models.CharField(max_length=64)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	game = models.ForeignKey(Game)
	money = models.PositiveIntegerField(default=0)

	def add_message(self, **kwargs):
		"""
		Send a message to the player
		"""
		m = Message.objects.create(**kwargs)
		m.save()
		m.recipient_set.add(self)

		return m

	def add_note(self, **kwargs):
		"""
		Create a note for the player
		"""
		m = self.add_message(flag=Message.NOTE, author=None, **kwargs)

		return m

	def get_current_orders(self):
		"""
		Returns the list of order for this turn
		"""
		return self.order_set.filter(turn=self.game.current_turn)

	def get_current_orders_cost(self):
		"""
		Get the cost for all orders on this turn
		"""
		return sum([order.cost for order in self.get_current_orders()])

	def build_order_message(self):
		"""
		Retrieve all orders for this turn, and build a message to remember them.
		"""
		orders = self.order_set.all()
		message = "# Ordres de %s pour le tour %s\n\n" % (self.name, self.game.current_turn)
		for order in orders:
			# Retrieve associated order:
			details = getattr(order, order.type.lower())
			message += "* %s\n" % details.description()

		message += "\nArgent initial : %s\nArgent restant: %s" % (self.money, self.money - self.get_current_orders_cost())

		return self.add_message(
			title="Ordres pour le tour %s" % self.game.current_turn,
			content=message,
			author=None,
			flag=Message.ORDER
		)

	def build_resolution_message(self):
		"""
		Retrieve all notes, and build a message to remember them.
		"""
		messages = Message.objects.filter(flag=Message.NOTE, recipient_set=self).order_by('title')
		resolution_message = u"### Résolution du tour %s ###" % self.game.current_turn
		past_title=""
		for message in messages:
			current_title=message.title
			if current_title==past_title:
				resolution_message += u"%s\n" % message.content
			else:
				resolution_message += u"\n[b]%s[/b]\n%s\n" % (message.title, message.content) #Change Bold title if this isn't right
			past_title=current_title
		return self.add_message(
			title="Informations personnelles du tour %s" % self.game.current_turn,
			content=resolution_message,
			author=None,
			flag=Message.RESOLUTION
		)

	def __unicode__(self):
		return self.name


class Message(models.Model):
	ORDER = 'OR'
	PRIVATE_MESSAGE = 'PM'
	RESOLUTION = 'RS'
	GLOBAL_NOTE = 'GN'
	GLOBAL_RESOLUTION = 'GR'
	NOTE = 'NO'

	MESSAGE_CHOICES = (
		('OR', 'Order'),
		('PM', 'Private Message'),
		('RS', 'Resolution Sheet'),
		('GR', 'Global Resolution'),
		('GN', 'Global Note'),
		('NO', 'Note'),
	)

	title = models.CharField(max_length=256)
	content = models.TextField(blank=True)
	author = models.ForeignKey(Player, null=True)
	public = models.BooleanField(default=False)
	recipient_set = models.ManyToManyField('Player', related_name="+")
	flag = models.CharField(max_length=2, choices=MESSAGE_CHOICES)


class Order(models.Model):
	player = models.ForeignKey(Player)
	turn = models.PositiveSmallIntegerField(editable=False)
	cost = models.PositiveSmallIntegerField(editable=False) # TODO : recompute from inheritance
	type = models.CharField(max_length=80, blank=True, editable=False)

	def save(self):
		# Save the current type to inflate later
		# self.type = '%s.%s' % (self._meta.app_label, self._meta.object_name)
		self.type = self._meta.object_name

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
		"""
		Resolve the order now
		"""
		raise NotImplementedError("Abstract call.")

	def get_cost(self):
		return 0

	def __unicode__(self):
		return "%s for %s, turn %s" % (self.type, self.player, self.turn)

	def description(self):
		"""
		Should return a full description of the order
		"""
		raise NotImplementedError("Abstract call.")

# Import datas for all engine_modules
from engine.modules import *

# Import signals
from engine.signals import *
