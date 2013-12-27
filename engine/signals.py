from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from django.db import IntegrityError
from engine.models import Game, Player, Message, Order
from engine.dispatchs import post_create


@receiver(post_save)
def send_post_create_signal(sender, instance, created, **kwargs):
	"""
	Send signal post_create when a model is created
	"""

	if created:
		del kwargs['signal']
		post_create.send(sender=sender, instance=instance, **kwargs)


@receiver(pre_save, sender=Game)
def check_current_turn_less_or_equal_total_turn(sender, instance, **kwargs):
	"""
	Can't save a Game with a current turn > total_turn
	"""
	if instance.current_turn > instance.total_turn:
		raise IntegrityError("current turn is greater than total turn")


@receiver(m2m_changed, sender=Message.recipient_set.through)
def check_player_is_in_the_same_game_than_author(sender, instance, action, **kwargs):
	if action == "pre_add":
		for player in  kwargs['pk_set']:
			if instance.author.game != Player.objects.get(pk=player).game:
				raise IntegrityError("the player is not in the same game than the author")


@receiver(pre_save, sender=Order)
def check_order_created_modifed_only_at_current_turn(sender, instance, **kwargs):
	"""
	Order can't be created / modified for another turn than current one
	"""
	if instance.turn != instance.player.game.current_turn:
		raise IntegrityError("can't create or modify for another turn than current one")


@receiver(pre_save, sender=Player)
def check_money_cant_be_negative(sender, instance, **kwargs):
	"""
	Players can't have negative money
	"""
	if instance.money < 0:
		raise IntegrityError("money can't be negative")
