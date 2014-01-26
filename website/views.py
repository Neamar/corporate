from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from engine.models import Game


def index(request):
	return render(request, 'index.html', {})


def get_game(request, game_id):
	"""
	Retrieve a game.
	Returns 404 exception if the user has no access to this game, or the game does not exists.
	"""
	return get_object_or_404(Game, pk=game_id, player_set__user=request.user)


@login_required
def orders(request, game_id):
	return get_game(request, game_id)
