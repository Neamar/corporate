# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.db.models import Sum, Q
from django.conf import settings
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from engine.dispatchs import validate_order, game_event


class Game(models.Model):
	# City name
	city = models.CharField(max_length=50)

	current_turn = models.PositiveSmallIntegerField(default=1)
	total_turn = models.PositiveSmallIntegerField(default=8)

	# Useful for testing, ensure results can be reproduced and understood easily.
	disable_side_effects = models.BooleanField(default=False, help_text="Disable all side effects (invisible hand, first and last effects, ...)")

	started = models.DateTimeField(auto_now_add=True)

	# List of possible events
	VOICE_UP = 'VOICE_UP'
	VOICE_DOWN = 'VOICE_DOWN'
	FIRST_EFFECT = 'FIRST_EFFECT'
	LAST_EFFECT = 'LAST_EFFECT'
	CRASH_EFFECT = 'CRASH_EFFECT'
	CORPORATION_CRASHED = 'CORPORATION_CRASHED'
	OPE_SABOTAGE = 'OPE_SABOTAGE'
	OPE_SABOTAGE_FAIL = 'OPE_SABOTAGE_FAIL'
	OPE_DATASTEAL_UP = 'OPE_DATASTEAL_UP'
	OPE_DATASTEAL_FAIL_UP = 'OPE_DATASTEAL_FAIL_UP'
	OPE_DATASTEAL_FAIL_DOWN = 'OPE_DATASTEAL_FAIL_DOWN'
	OPE_DATASTEAL_DOWN = 'OPE_DATASTEAL_DOWN'
	OPE_PROTECTION = 'OPE_PROTECTION'
	OPE_EXTRACTION_UP = 'OPE_EXTRACTION_UP'
	OPE_EXTRACTION_FAIL_UP = 'OPE_EXTRACTION_FAIL_UP'
	OPE_EXTRACTION_FAIL_DOWN = 'OPE_EXTRACTION_FAIL_DOWN'
	OPE_EXTRACTION_DOWN = 'OPE_EXTRACTION_DOWN'
	EFFECT_CONTRAT_UP = 'EFFECT_CONTRAT_UP'
	EFFECT_CONTRAT_DOWN = 'EFFECT_CONTRAT_DOWN'
	MARKET_HAND_UP = 'MARKET_HAND_UP'
	MARKET_HAND_DOWN = 'MARKET_HAND_DOWN'
	ADD_CITIZENSHIP = 'ADD_CITIZENSHIP'
	REMOVE_CITIZENSHIP = 'REMOVE_CITIZENSHIP'
	IC_UP = 'IC_UP'
	OPE_INFORMATION = 'OPE_INFORMATION'
	EFFECT_CONSOLIDATION_UP = 'EFFECT_CONSOLIDATION_UP'
	EFFECT_CONSOLIDATION_DOWN = 'EFFECT_CONSOLIDATION_DOWN'
	EFFECT_SECURITY_UP = 'EFFECT_SECURITY_UP'
	EFFECT_SECURITY_DOWN = 'EFFECT_SECURITY_DOWN'
	SPECULATION_WIN = 'SPECULATION_WIN'
	SPECULATION_LOST = 'SPECULATION_LOST'
	WIRETRANSFER = 'WIRETRANSFER'
	BUY_SHARE = 'BUY_SHARE'
	VOTE_CONSOLIDATION = 'VOTE_CONSOLIDATION'
	VOTE_SECURITY = 'VOTE_SECURITY'
	VOTE_CONTRAT = 'VOTE_CONTRAT'
	MONEY_NEXT_TURN = 'MONEY_NEXT_TURN'
	BACKGROUND = 'BACKGROUND'
	GAIN_DOMINATION_BUBBLE = 'GAIN_DOMINATION_BUBBLE'
	LOSE_DOMINATION_BUBBLE = 'LOSE_DOMINATION_BUBBLE'
	GAIN_NEGATIVE_BUBBLE = 'GAIN_NEGATIVE_BUBBLE'
	LOSE_NEGATIVE_BUBBLE = 'LOSE_NEGATIVE_BUBBLE'

	def add_event(self, event_type, data, delta=0, corporation=None, players=[], corporation_market=None):
		"""
		Create a game event signal. This signal may be received for a log creation for example.
		"""
		game_event.send(
			sender=self.__class__,
			event_type=event_type,
			data=data,
			delta=delta,
			corporation=corporation,
			corporation_market=corporation_market,
			players=players,
			instance=self
		)

	@transaction.atomic
	def resolve_current_turn(self):
		"""
		Resolve all orders for this turn, increment current_turn by 1.
		"""
		# Execute all tasks
		from engine.modules import tasks_list
		for Task in tasks_list:
			# print "* [%s] **%s** : %s" % (Task.RESOLUTION_ORDER, Task.__name__, Task.__doc__.strip())
			t = Task()
			t.run(self)

		# Build resolution messages for each player
		for player in self.player_set.all().select_related('game'):
			player.build_resolution_message()

		# Increment current turn and terminate.
		self.current_turn += 1
		self.save()

	@transaction.atomic
	def initialise_game(self):
		"""
		Resolve all the tasks that must be solved at initialisation
		We must go back on turn 0 to update bubbles
		"""
		self.current_turn = 0
		self.save()
		from engine.modules import initialisation_tasks_list
		for Task in initialisation_tasks_list:
			t = Task()
			t.run(self)

		self.current_turn = 1
		self.save()

	@property
	def corporation_set(self):
		return self.all_corporation_set.filter(game=self).filter(Q(crash_turn=self.current_turn) | Q(crash_turn__isnull=True))

	def __unicode__(self):
		return u"Corporate Game: %s" % self.city


class Player(models.Model):
	class Meta:
		unique_together = (("game", "user"),)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	game = models.ForeignKey(Game)

	name = models.CharField(max_length=64)
	money = models.PositiveIntegerField(default=2000)
	background = models.CharField(max_length=50)
	rp = models.TextField(default="", blank=True)
	secrets = models.TextField(default="", blank=True)

	@property
	def influence(self):
		"""
		Return player's influence at current turn
		"""
		# Influence for the turn is on preceding turn's Influence object
		influence = self.influence_set.get(turn=self.game.current_turn - 1)
		return influence

	def get_influence(self, turn=None):
		"""
		Return player's influence at specified turn
		Yes, this is a little redundant, but I need to have it for any arbitrary turn, and
		I thought it would be good to discuss it before breaking the "influence" property
		"""

		if turn is None:
			turn = self.game.current_turn

		# Influence for the turn is on preceding turn's Influence object
		influence = self.influence_set.get(turn=turn - 1)
		return influence

	@property
	def citizenship(self):
		"""
		Return player's citizenship at current turn
		"""
		# Citizenship for the turn is on preceding turn's Citizenship object
		citizenship = self.citizenship_set.get(turn=self.game.current_turn - 1)
		return citizenship

	def get_current_orders(self):
		"""
		Returns the list of order for this turn
		"""
		return self.order_set.filter(turn=self.game.current_turn)

	def get_current_orders_cost(self):
		"""
		Get the cost for all player orders' on this turn
		"""
		return self.get_current_orders().aggregate(Sum('cost'))['cost__sum'] or 0

	def build_resolution_message(self):
		"""
		Retrieve all notes addressed to the player for this turn, and build a message to remember them.
		"""
		# Start by adding the final note
		m = "TODO"
		return m

	def __unicode__(self):
		return self.name


class Order(models.Model):
	title = "Ordre"

	player = models.ForeignKey(Player)

	turn = models.PositiveSmallIntegerField(editable=False)
	cost = models.PositiveSmallIntegerField(editable=False)
	type = models.CharField(max_length=40, blank=True, editable=False)

	def save(self, **kwargs):
		# Save the current type to inflate later (model inheritance can be tricky)
		self.type = self._meta.object_name

		# Turn default value is `game.current_turn`
		if not self.turn:
			self.turn = self.player.game.current_turn

		if not self.cost:
			self.cost = self.get_cost()

		super(Order, self).save(**kwargs)

	def clean(self):
		"""
		Emit a validate_order signal to ensure the order is valid and can be saved
		"""
		if self.__class__.__name__ == "Order":
			raise ValidationError("You can't save raw Order, only subclasses")
		validate_order.send(sender=self.__class__, instance=self)
		super(Order, self).clean()

	def resolve(self):
		"""
		Resolve the order now
		"""
		raise NotImplementedError("Abstract call.")

	def get_cost(self):
		return 0

	def __unicode__(self):
		return u"%s for %s, turn %s" % (self.type, self.player, self.turn)

	def description(self):
		"""
		Should return a full description of the order
		"""
		raise NotImplementedError("Abstract call.")

	def get_form(self, data=None):
		"""
		Retrieve a Django form to create / edit this order.
		Default behavior is to instantiate a new item from `get_form_class()`
		"""
		return self.get_form_class()(data, instance=self)

	def get_form_class(self):
		"""
		Build a new class for Order form.
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
		In most case, we need to subclass all those orders to their correct orders type,
		and this function will convert a plain Order to the most specific Order subclass
		according to the stored `.type`.
		"""
		from engine.modules import orders_list

		for ChildOrder in orders_list:
			if ChildOrder.__name__ == self.type:
				return ChildOrder.objects.get(pk=self.pk)

		raise LookupError("No orders subclass match this base: %s" % self.type)

	def custom_description(self):
		"""
		A custom description, that may be displayed in some places (for instance, orders list page)
		"""
		return ""

# Import data for all engine_modules
from engine.modules import *

# Import signals
from engine.signals import *
