from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db import IntegrityError

from messaging.models import Message


@receiver(m2m_changed, sender=Message.recipient_set.through)
def check_player_is_in_the_same_game_than_author(sender, instance, action, model, **kwargs):
	if action == "pre_add":
		for player in  kwargs['pk_set']:
			if instance.author is not None and instance.author.game != model.objects.get(pk=player).game:
				raise IntegrityError("The player is not in the same game than the author.")
