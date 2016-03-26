from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import IntegrityError

from engine.exceptions import OrderNotAvailable
from engine.dispatchs import validate_order
from engine.models import Game, Player, Order
from engine.dispatchs import post_create


@receiver(post_save)
def send_post_create_signal(sender, instance, created, **kwargs):
	"""
	Send signal post_create when a model is first created
	"""
	if created:
		del kwargs['signal']
		post_create.send(sender=sender, instance=instance, **kwargs)


@receiver(post_save, sender=Game)
def game_initialisation(sender, instance, created, **kwargs):
	"""
	Start the tasks once the game is created
	"""
	if created:
		instance.initialise_game()


@receiver(post_create, sender=Player)
def add_player_on_game(sender, instance, **kwargs):
	"""
	Send an event on each player to remind him what is his secret at the start of the game
	"""
	instance.game.add_event(event_type=Game.BACKGROUND_REMINDER, data={"background": instance.background, "player": instance.name}, players=[instance])


@receiver(pre_save, sender=Game)
def check_current_turn_less_or_equal_total_turn(sender, instance, **kwargs):
	"""
	Can't save a Game with a current turn > total_turn
	"""
	if instance.current_turn > instance.total_turn:
		raise IntegrityError("current turn is greater than total turn")


@receiver(pre_save, sender=Order)
def check_order_created_modifed_only_at_current_turn(sender, instance, **kwargs):
	"""
	Order can't be created / modified for another turn than current one
	"""
	if instance.turn != instance.player.game.current_turn:
		raise IntegrityError("Can't create or modify for another turn than current one.")


@receiver(pre_save, sender=Player)
def check_money_cant_be_negative(sender, instance, **kwargs):
	"""
	Players can't have negative money
	"""
	if instance.money < 0:
		raise IntegrityError("Money can't be negative.")


@receiver(validate_order)
def buy_order_require_money(sender, instance, **kwargs):
	"""
	Check player has enough money for this order
	"""
	if instance.get_cost() + instance.player.get_current_orders_cost() > instance.player.money:
		raise OrderNotAvailable("Pas assez d'argent pour lancer cet ordre.")
