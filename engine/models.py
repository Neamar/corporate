# -*- coding: utf-8 -*-
from django import forms
from django.db import models, transaction
from django.db.models import Sum, Q
from django.conf import settings
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from engine.dispatchs import validate_order, game_event
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID
from utils.image_treatment import preprocess


class Game(models.Model):
	# City name

	STATUS = (
		(u'created', u'created'),
		(u'started', u'started'),
		(u'ended', u'ended'),
	)

	city = models.CharField(max_length=50)

	current_turn = models.PositiveSmallIntegerField(default=1)
	total_turn = models.PositiveSmallIntegerField(default=7)

	# Useful for testing, ensure results can be reproduced and understood easily.
	disable_side_effects = models.BooleanField(default=False, help_text="Disable all side effects (invisible hand, first and last effects, ...)")

	created = models.DateTimeField(auto_now_add=True)
	status = models.CharField(default="created", choices=STATUS, max_length=50)
	last_update = models.DateTimeField(default=None, blank=True, null=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)  # The creator who can start the game and resolve turns
	password = models.CharField(max_length=128, blank=True, null=True)  # to filter the game to people you want in

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
	BACKGROUND_REMINDER = 'BACKGROUND_REMINDER'
	GAIN_DOMINATION_BUBBLE = 'GAIN_DOMINATION_BUBBLE'
	LOSE_DOMINATION_BUBBLE = 'LOSE_DOMINATION_BUBBLE'
	GAIN_NEGATIVE_BUBBLE = 'GAIN_NEGATIVE_BUBBLE'
	LOSE_NEGATIVE_BUBBLE = 'LOSE_NEGATIVE_BUBBLE'

	def add_event(self, event_type, data, delta=0, corporation=None, players=[], corporation_market=None, turn=None):
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
			instance=self,
			turn=turn
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

		# Increment current turn and terminate.
		self.current_turn += 1
		self.last_update = timezone.now()
		self.save()

	@transaction.atomic
	def initialise_game(self):
		"""
		Resolve all the tasks that must be solved at initialisation
		We must go back on turn 0 to update bubbles
		We set back current turn to 1 afterwards to start the game as the turn 0 is finished
		"""
		self.current_turn = 0
		self.save()
		from engine.modules import initialisation_tasks_list
		for Task in initialisation_tasks_list:
			# print "* [%s] **%s** : %s" % (Task.RESOLUTION_ORDER, Task.__name__, Task.__doc__.strip())
			t = Task()
			t.run(self)

		self.current_turn = 1
		self.save()

	def start_game(self):
		"""
		Once a game is started, new players can't join it and players can't update their basic informations profile anymore
		"""
		if self.status == 'created':
			self.status = 'started'
			self.save()

	@property
	def corporation_set(self):
		return self.all_corporation_set.filter(game=self).filter(Q(crash_turn=self.current_turn) | Q(crash_turn__isnull=True))

	@property
	def started(self):
		if self.status == 'created':
			return False
		else:
			return True

	def __unicode__(self):
		return u"Corporate Game: %s" % self.city


class GameForm(ModelForm):
	class Meta:
		model = Game
		fields = ['city', 'password']


class Player(models.Model):
	class Meta:
		unique_together = (("game", "user"),)

	# Enumerate the party lines and their meanings
	BACKGROUNDS = (
		(u'Anonyme', u'Anonyme'),
		(u'Acharné', u'Acharné'),
		(u'Analyste', u'Analyste'),
		(u'Altruisite', u'Altruisite'),
		(u'Corrupteur', u'Corrupteur'),
		(u'Dévoué', u'Dévoué'),
		(u'Flambeur', u'Flambeur'),
		(u'Grande geule', u'Grande geule'),
		(u'Oligarque', u'Oligarque'),
		(u'Pacifiste', u'Pacifiste'),
		(u'Paranoïaque', u'Paranoïaque'),
		(u'Protecteur', u'Protecteur'),
		(u'Pyromane', u'Pyromane'),
		(u'Traître', u'Traître'),
		(u'Violent', u'Violent'),
		(u'Vénal', u'Vénal'),
	)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	game = models.ForeignKey(Game)

	name = models.CharField(max_length=64)
	money = models.PositiveIntegerField(default=2000)
	background = models.CharField(default="Anonyme", choices=BACKGROUNDS, max_length=50)
	rp = models.TextField(default="", blank=True)
	secrets = models.TextField(default="", blank=True)

	avatar = StdImageField(upload_to=UploadToUUID(path='avatars'), variations={
		'thumbnail': {"width": 55, "height": 55, "crop": True}
	}, render_variations=preprocess)

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

	def __unicode__(self):
		return self.name


class PlayerForm(ModelForm):
	password = forms.CharField(max_length=128, required=False)

	class Meta:
		model = Player
		fields = ['password', 'name', 'background', 'rp', 'avatar']

	def __init__(self, *args, **kwargs):
		self.game_password = kwargs.pop('game_password', None)
		super(PlayerForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		# On n'a pas à rentrer de mot de passe si on est déjà inscrit sur la partie ou que le mot de passe sur la game est vide
		if instance and (instance.pk or self.game_password is None):
			del self.fields['password']
		if instance and instance.pk and instance.game.started is True:
				self.fields['name'].widget.attrs['readonly'] = True
				self.fields['background'].widget.attrs['readonly'] = True
				self.fields['avatar'].widget.attrs['disabled'] = True

	def clean_password(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			return ''
		else:
			data = self.cleaned_data['password']
			if data != self.game_password:
				raise forms.ValidationError("Le mot de passe est incorrect")

	def clean_name(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk and instance.game.started is True:
			return instance.name
		else:
			return self.cleaned_data['name']

	def clean_background(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk and instance.game.started is True:
			return instance.background
		else:
			return self.cleaned_data['background']

	def clean_avatar(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk and instance.game.started is True:
			return instance.avatar
		else:
			return self.cleaned_data['avatar']
	

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
