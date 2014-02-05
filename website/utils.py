from django.shortcuts import get_object_or_404

from engine.models import Player


def get_player(request, game_id):
	"""
	Retrieve a player associated with the user and the game.
	Returns 404 exception if the user has no access to this game, or the game does not exists.
	"""
	return get_object_or_404(Player, user=request.user, game=game_id)
