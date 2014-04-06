# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.conf import settings
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from engine.dispatchs import validate_order
from messaging.models import Message, Note, Newsfeed
from utils.read_markdown import read_file_from_path


class Game(models.Model):
	city = models.CharField(max_length=50)
	current_turn = models.PositiveSmallIntegerField(default=1)
	total_turn = models.PositiveSmallIntegerField(default=8)
	disable_side_effects = models.BooleanField(default=False, help_text="Disable all side effects (invisible hand, first and last effects, ...)")
	started = models.DateTimeField(auto_now_add=True)

	@transaction.atomic
	def resolve_current_turn(self):
		"""
		Resolve all orders for this turn, increment current_turn by 1.
		"""
		# Execute all tasks
		from engine.modules import tasks_list
		for task in tasks_list:
			# print "* [%s] **%s** : %s" % (task.RESOLUTION_ORDER, task.__name__, task.__doc__.strip())
			t = task()
			t.run(self)

		# Build resolution messages for each player
		for player in self.player_set.all():
			player.build_resolution_message()
		Note.objects.filter(recipient_set__game=self).delete()

		# Increment current turn and terminate.
		self.current_turn += 1
		self.save()

	def add_newsfeed(self, **kwargs):
		"""
		Create a newsfeed on the game
		"""
		n = Newsfeed.objects.create(turn=self.current_turn, game=self, **kwargs)
		return n

	def add_newsfeed_from_template(self, category, path, **kwargs):
		"""
		Construct the content of a newsfeed, avoiding messages already displayed within the same game.
		"""
		message_number = Newsfeed.objects.filter(category=category, game=self, path=path).count() + 1

		try:
			content = read_file_from_path("%s/datas/newsfeeds/%s/%s/%s.md" % (settings.BASE_DIR, category, path, message_number))
		except IOError:
			content = read_file_from_path("%s/datas/newsfeeds/%s/%s/_.md" % (settings.BASE_DIR, category, path))

		kwargs['content'] = content
		kwargs['category'] = category
		kwargs['path'] = path
		self.add_newsfeed(**kwargs)

	def __unicode__(self):
		return "Corporate Game: %s" % self.city


class Player(models.Model):
	class Meta:
		unique_together = (("game", "user"),)

	name = models.CharField(max_length=64)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	game = models.ForeignKey(Game)
	money = models.PositiveIntegerField(default=2000)
	background = models.CharField(default=None, blank=True, null=True, max_length=150)
	secrets = models.TextField(default="", blank=True)

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

	def build_resolution_message(self):
		"""
		Retrieve all notes addressed to the player for this turn, and build a message to remember them.
		"""
		notes = Note.objects.filter(recipient_set=self, turn=self.game.current_turn)
		m = Message.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=notes,
			title="Message de résolution du tour %s" % self.game.current_turn,
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
	cost = models.PositiveSmallIntegerField(editable=False)
	type = models.CharField(max_length=40, blank=True, editable=False)

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

	def get_form(self, datas=None):
		"""
		Retrieve a form to create / edit this order
		"""
		return self.get_form_class()(datas, instance=self)

	def get_form_class(self):
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

	def to_child(self):
		"""
		By default, when we do player.order_set.all(), we retrieve Order instance.
		In most case, we need to subclass all those orders to their correct orders type, and this function will convert a plain Order to the most specific Order subclass according to the stored `.type`.
		"""
		from engine.modules import orders_list

		for ChildOrder in orders_list:
			if ChildOrder.__name__ == self.type:
				return ChildOrder.objects.get(pk=self.pk)

		raise LookupError("No orders subclass match this base: %s" % self.type)


# Import datas for all engine_modules
from engine.modules import *

# Import signals
from engine.signals import *
