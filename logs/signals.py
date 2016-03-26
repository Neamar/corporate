import json
from logs.models import Log, ConcernedPlayer
from django.dispatch import receiver
from engine.dispatchs import game_event


@receiver(game_event)
def insert_log_database(sender, instance, event_type, data, delta=0, corporation=None, corporation_market=None, turn=None, players=[], **kwargs):
	# We deduce the value of property hide_for players from the category
	hide_for_players = event_type in Log.HIDE_FOR_PLAYERS

	# Same thing for public property : we deduce it from the category
	public = event_type in Log.PUBLIC

	# Same thing for transmittable property attached on the many-to-many
	transmittable = event_type not in Log.UNTRANSMITTABLE

	# Message building
	message = json.dumps(data)

	if turn is None:
		turn = instance.current_turn
	# creation of the log
	log = Log.objects.create(
		turn=turn,
		game=instance,
		delta=delta,
		event_type=event_type,
		data=message,
		corporation=corporation,
		corporation_market=corporation_market,
		hide_for_players=hide_for_players,
		public=public
	)

	# many-to-many for players
	cps = []
	for player in players:
		cp = ConcernedPlayer(
				player=player,
				log=log,
				transmittable=transmittable,
				personal=True
		)
		cps.append(cp)
	ConcernedPlayer.objects.bulk_create(cps)
