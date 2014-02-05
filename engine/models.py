# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from engine.dispatchs import validate_order
from messaging.models import Message, Note

class Game(models.Model):
	city = models.CharField(max_length=50)
	current_turn = models.PositiveSmallIntegerField(default=1)
	total_turn = models.PositiveSmallIntegerField(default=8)
	started = models.DateTimeField(auto_now_add=True)

	def resolve_current_turn(self):
		"""
		Resolve all orders for this turn, increment current_turn by 1.
		"""

		# First step: build a message for each player containing order list.
		for player in self.player_set.all():
			player.build_order_message()

		# Execute all tasks
		from engine.modules import tasks_list
		for task in tasks_list:
			t = task()
			t.run(self)

		# Build resolution messages for each player
		for player in self.player_set.all():
			player.build_resolution_message()
		Note.objects.filter(recipient_set__game=self).delete()

		# Increment current turn and terminate.
		self.current_turn += 1
		self.save()

	def add_note(self, **kwargs):
		"""
		Create a note, to be used later for the resolution message
		"""
		n = Note.objects.create(turn=self.current_turn, **kwargs)
		n.recipient_set = self.player_set.all()
		return n

	def __unicode__(self):
		return "Corporate Game: %s" % self.city


class Player(models.Model):
	class Meta:
		unique_together = (("game", "user"),)

	name = models.CharField(max_length=64)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	game = models.ForeignKey(Game)
	money = models.PositiveIntegerField(default=2000)

	def add_message(self, **kwargs):
		"""
		Send a message to the player
		"""
		m = Message(turn=self.game.current_turn, **kwargs)
		m.save()
		m.recipient_set.add(self)

		return m

	def add_note(self, **kwargs):
		"""
		Create a note for the player
		"""
		n = Note(turn=self.game.current_turn, **kwargs)
		n.save()
		n.recipient_set.add(self)

		return n

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
			try:
				details = getattr(order, order.type.lower())
			except AttributeError:
				try:
					# TODO : CHANGE DAT SHIT
					details = getattr(order.runorder, order.type.lower())
				except AttributeError:
					# TODO : CHANGE DAT SHIT (again)
					details = getattr(order.runorder.offensiverunorder, order.type.lower())

			message += "* %s\n" % details.description()

		message += "\nArgent initial : %s\nArgent restant: %s" % (self.money, self.money - self.get_current_orders_cost())

		return self.add_message(
			title="Ordres du tour",
			content=message,
			author=None,
			flag=Message.ORDER,
		)

	def build_resolution_message(self):
		"""
		Retrieve all notes addressed to the player for this turn, and build a message to remember them.
		"""
		notes = Note.objects.filter(recipient_set=self, turn=self.game.current_turn)
		m = Message.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=notes,
			opening=u"# Résolution du tour %s\n" % self.game.current_turn,
			title="Informations personnelles du tour %s" % self.game.current_turn,
			turn=self.game.current_turn
		)
		m.recipient_set.add(self)
		return m

	def __unicode__(self):
		return self.name


class Order(models.Model):
	title = "Ordre"

	player = models.ForeignKey(Player)
	turn = models.PositiveSmallIntegerField(editable=False)
	cost = models.PositiveSmallIntegerField(editable=False) # TODO : recompute from inheritance
	type = models.CharField(max_length=80, blank=True, editable=False)

	def save(self):
		# Save the current type to inflate later
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

	def get_form(self):
		"""
		Retrieve a form to create / edit this order
		"""
		return self.form_class()(instance=self)

	def form_class(self):
		"""
		Build a new class for forms,
		"""
		class OrderForm(ModelForm):
			class Meta(self.get_form_meta()):
				pass

		return OrderForm

	def get_form_meta(self):
		"""
		Meta class to use for get_form()
		"""
		class Meta:
			model = self.__class__
			exclude = ['player']

		return Meta
# Import datas for all engine_modules
from engine.modules import *

# Import signals
from engine.signals import *
