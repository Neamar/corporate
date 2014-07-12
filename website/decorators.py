from functools import wraps
from django.shortcuts import render as django_render
from django.http import Http404

from website.utils import get_player


def render(page):
	"""
	Render the page with returned dict.
	"""

	def decorator(func):
		@wraps(func)
		def wrap(request, *args, **kwargs):
			response = func(request, *args, **kwargs)
			if isinstance(response, dict):
				return django_render(request, page, response)
			else:
				return response
		return wrap
	return decorator


def find_player_from_game_id(func):
	@wraps(func)
	def wrap(request, game_id, **kwargs):
		player = get_player(request, game_id)
		game = player.game

		return func(request, game=game, player=player, **kwargs)
	return wrap


def inject_game_into_response(func):
	@wraps(func)
	def wrap(*args, **kwargs):
		response = func(*args, **kwargs)
		if isinstance(response, dict):
			response['game'] = kwargs["game"]
		return response
	return wrap


def turn_by_turn_view(func):
	"""
	Decorator for view that let user browse data page by page.
	Should be chained after @find_player_from_game_id.
	"""
	@wraps(func)
	def wrap(request, game, player, turn=None, *args, **kwargs):
		if turn is None:
			turn = game.current_turn - 1
		turn = int(turn)

		if turn >= game.current_turn:
			raise Http404("This turn has not yet been played.")

		response = func(request=request, game=game, player=player, turn=turn, *args, **kwargs)
		if isinstance(response, dict):
			response['current_turn'] = turn
			response['turns'] = range(1, game.current_turn)
		return response
	return wrap
