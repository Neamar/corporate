from django.shortcuts import render as django_render

from website.utils import get_player


def render(page):
	"""
	Render the page with returned dict.
	"""

	def decorator(func):
		def wrap(request, *args, **kwargs):
			response = func(request, *args, **kwargs)
			if isinstance(response, dict):
				return django_render(request, page, response)
			else:
				return response
		return wrap
	return decorator


def find_player_from_game_id(func):
	def wrap(request, game_id, **kwargs):
		player = get_player(request, game_id)
		game = player.game

		return func(request, game=game, player=player, **kwargs)
	return wrap


def inject_game_into_response(func):
	def wrap(*args, **kwargs):
		response = func(*args, **kwargs)
		if isinstance(response, dict):
			response['game'] = kwargs["game"]
		return response
	return wrap
