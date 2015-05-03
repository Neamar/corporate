from logs.models import Logs, ConcernedPlayers
from django.dispatch import receiver, Signal
from engine.dispatchs import game_event

@receiver(game_event)
def insert_log_database(sender, instance, event_type, data, delta=0, corporation=None, corporationmarket=None, players=None, **kwargs):
	# We deduce the value of property hidden_for players of the category
	hide_for_players = (event_type in Logs.HIDE_FOR_PLAYERS)

	# Same thing for public property : we deduce it of the category
	public = (event_type in Logs.PUBLIC)

	# Same thing for transmittable propery attached on the many-to-many
	transmittable = (event_type not in Logs.UNTRANSMITTABLE)

	# creation of the log
	log = Logs.objects.create(
		turn=instance.current_turn,
		game=instance,
		delta=delta,
		event_type=event_type,
		data=data,
		corporation=corporation,
		corporationmarket=corporationmarket,
		hide_for_players=hide_for_players,
		public=public
	)

	# many-to-many for players
	if players!=None:
		cps = []
		for player in players:
			cp = ConcernedPlayers(
					player=player,
					log=log,
					transmittable=transmittable,
					personal=True)
			cps.append(cp)
		ConcernedPlayers.objects.bulk_create(cps)
