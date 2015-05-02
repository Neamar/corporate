# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.db.models import Sum
from django.conf import settings
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from engine.dispatchs import validate_order, game_event
from messaging.models import Message, Note, Newsfeed
from utils.read_markdown import read_file_from_path


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
	WIN_BUBBLE = 'WIN_BUBBLE'
	LOST_BUBBLE = 'LOST_BUBBLE'

	EVENTS = (
		(VOICE_UP, 'Voix au chapitre positive'),
		(VOICE_DOWN, 'Voix au chapitre négative'),
		(FIRST_EFFECT, 'Effet premier'),
		(LAST_EFFECT, 'Effet dernier'),
		(CRASH_EFFECT, 'Effet crash'),
		(OPE_SABOTAGE, 'Opération de sabotage réussie'),
		(OPE_SABOTAGE_FAIL, 'Opération de sabotage échouée'),
		(OPE_DATASTEAL_UP, 'Opération de datasteal réussie positive'),
		(OPE_DATASTEAL_FAIL_UP, 'Opération de datasteal échouée positive'),
		(OPE_DATASTEAL_FAIL_DOWN, 'Opération de datasteal échouée négative'),
		(OPE_DATASTEAL_DOWN, 'Opération de datasteal réussie négative'),
		(OPE_PROTECTION, 'Opération de protection'),
		(OPE_EXTRACTION_UP, 'Opération d\'extraction réussie positive'),
		(OPE_EXTRACTION_FAIL_UP, 'Opération d\'extraction échouée positive'),
		(OPE_EXTRACTION_FAIL_DOWN, 'Opération d\'extraction échouée négative'),
		(OPE_EXTRACTION_DOWN, 'Opération d\'extraction réussie négative'),
		(EFFECT_CONTRAT_UP, 'Effet de Detroit Inc. Contrat public positif'),
		(EFFECT_CONTRAT_DOWN, 'Effet de Detroit Inc. Contrat public négatif'),
		(MARKET_HAND_UP, 'Main du marché positive'),
		(MARKET_HAND_DOWN, 'Main du marché négative'),
		(ADD_CITIZENSHIP, 'Ajout de citoyenneté'),
		(REMOVE_CITIZENSHIP, 'Perte de citoyenneté'),
		(IC_UP, 'Augmentation d\'influence corporatiste'),
		(OPE_INFORMATION, 'Opération d\'information'),
		(EFFECT_CONSOLIDATION_UP, 'Effet de Detroit Inc Consolidation positif'),
		(EFFECT_CONSOLIDATION_DOWN, 'Effet de Detroit Inc Consolidation négatif'),
		(EFFECT_SECURITY_UP, 'Effet de Detroit Inc Réforme de la sécuritée positif'),
		(EFFECT_SECURITY_DOWN, 'Effet de Detroit Inc Réforme de la sécuritée négatif'),
		(SPECULATION_WIN, 'Spéculation réussie'),
		(SPECULATION_LOST, 'Spéculation échouée'),
		(WIRETRANSFER, 'Transfert d\'argent à un autre joueur'),
		(BUY_SHARE, 'Acheter une part'),
		(VOTE_CONSOLIDATION, 'Vote de la ligne Consolidation à Detoit Inc.'),
		(VOTE_SECURITY, 'Vote de la ligne Réforme de la sécuritée à Detoit Inc.'),
		(VOTE_CONTRAT, 'Vote de la ligne contrat public à Detoit Inc.'),
		(MONEY_NEXT_TURN, 'Argent disponible au début de tour suivant'),
		(BACKGROUND, 'Information de background découverte'),
		(WIN_BUBBLE, 'Le marché a un actif de domination'),
		(LOST_BUBBLE, 'Le marché a un actif de perte sèche'),
	)

	def create_game_event(self, event_type, data, delta=0, corporation=None, players=None, corporationmarket=None):
		"""
		Create a game event signal. This signal may be received for a log creation for example.
		"""
		game_event.send(
			sender=self.__class__,
			event_type=event_type,
			data=data,
			delta=delta,
			corporation=corporation,
			players=players,
			corporationmarket=corporationmarket)

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
		# Remove all Notes
		Note.objects.filter(recipient_set__game=self).delete()

		# Increment current turn and terminate.
		self.current_turn += 1
		self.save()

	def add_newsfeed(self, players=None, corporations=None, **kwargs):
		"""
		Create a newsfeed on the game
		"""
		n = Newsfeed.objects.create(turn=self.current_turn, game=self, **kwargs)
		if players:
			n.players = players
		if corporations:
			n.corporations = corporations
		return n

	def add_newsfeed_from_template(self, category, path, **kwargs):
		"""
		Construct the content of a newsfeed, avoiding messages already displayed within the same game.
		"""
		message_number = Newsfeed.objects.filter(category=category, game=self, path=path).count() + 1

		try:
			content = read_file_from_path("%s/newsfeeds/%s/%s/%s.md" % (settings.CITY_BASE_DIR, category, path, message_number))
		except IOError:
			# We don't have enough files, revert to default
			content = read_file_from_path("%s/newsfeeds/%s/%s/_.md" % (settings.CITY_BASE_DIR, category, path))

		kwargs['content'] = content
		kwargs['category'] = category
		kwargs['path'] = path
		self.add_newsfeed(**kwargs)

	def __unicode__(self):
		return "Corporate Game: %s" % self.city


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

	@property
	def citizenship(self):
		"""
		Return player's citizenship at current turn
		"""
		# Citizenship for the turn is on preceding turn's Citizenship object
		citizenship = self.citizenship_set.get(turn=self.game.current_turn - 1)
		return citizenship

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
		Get the cost for all player orders' on this turn
		"""
		return self.get_current_orders().aggregate(Sum('cost'))['cost__sum'] or 0

	def build_resolution_message(self):
		"""
		Retrieve all notes addressed to the player for this turn, and build a message to remember them.
		"""
		# Start by adding the final note
		self.add_note(content="Argent disponible pour le tour : %sk¥" % self.money)

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
		# Save the current type to inflate later (model inheritance can be tricky)
		self.type = self._meta.object_name

		# Turn default value is `game.current_turn`
		if not self.turn:
			self.turn = self.player.game.current_turn

		if not self.cost:
			self.cost = self.get_cost()

		super(Order, self).save()

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
		return "%s for %s, turn %s" % (self.type, self.player, self.turn)

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


# Import data for all engine_modules
from engine.modules import *

# Import signals
from engine.signals import *
