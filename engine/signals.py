from django.db.models.signals import pre_delete, pre_save, post_save, m2m_changed
from django.dispatch import receiver

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from engine.models import Game, Player, Message, Order

print "global"

@receiver(pre_save, sender=Game)
def check_current_turn_less_or_equal_total_turn(sender, instance, **kwargs):
	"""
	Can't save a Game with a current turn > total_turn
	"""

	if instance.current_turn > instance.total_turn:
		raise IntegrityError("current_turn is greater than total_turn")


@receiver(m2m_changed, sender=Message.recipient_set.through)
def check_player_is_in_the_same_game_than_author(sender, instance, action, **kwargs):
	if action == "pre_add":
		print instance.author
		print instance.recipient_set

		#if instance.author != instance.

