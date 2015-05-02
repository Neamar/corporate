from logs.models import *
from django.dispatch import receiver
from engine.dispatchs import game_event


@receiver(game_event)
def insert_log_database(sender, event_type, category, data, delta=0, players=None, corporation=None, corporationmarket=None, **kwargs):
	# We deduce the value of property hidden_for players of the category
	hide_for_players = (category in logs.Logs.HIDE_FOR_PLAYERS)

	# Same thing for public property : we deduce it of the category
	public = (category in logs.Logs.PUBLIC)

	# Same thing for transmittable propery attached on the many-to-many
	transmittable = (category not in logs.Logs.NOT_TRANSMITTABLE)
	# creation of the log
	log = Logs.objects.create(
		turn=sender.current_turn,
		game=sender,
		delta=delta,
		event_type=event_type,
		data=data,
		corporation=corporation,
		corporationmarket=corporationmarket,
		hide_for_players=hide_for_players,
		public=public
	)

	# many-to-many for players
	cps = []
	for player in players:
		cp = ConcernedPlayers(
				player=player,
				log=log,
				transmittable=transmittable,
				personal=True)
		cps.append(cp)
	ConcernedPlayers.objects.bulk_create(cps)