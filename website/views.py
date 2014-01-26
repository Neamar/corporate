from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from engine.models import Game, Player
from engine.modules import orders_list
from engine.exceptions import OrderNotAvailable


def index(request):
	return render(request, 'index.html', {})


def get_game(request, game_id):
	"""
	Retrieve a game.
	Returns 404 exception if the user has no access to this game, or the game does not exists.
	"""
	return get_object_or_404(Game, pk=game_id, player__user=request.user)


def get_player(request, game_id):
	"""
	Retrieve a player associated with the user and the game.
	Returns 404 exception if the user has no access to this game, or the game does not exists.
	"""
	return get_object_or_404(Player, user=request.user, game=game_id)


@login_required
def orders(request, game_id):
	player = get_player(request, game_id)
	game = get_game(request, game_id)

	all_orders = [{"type": order, 'name': order.__name__} for order in orders_list]

	print all_orders

	for order in all_orders:
		instance = order["type"](player=player)
		try:
			instance.clean()
			order['available'] = True
		except OrderNotAvailable:
			order['available'] = False
		except:
			order['available'] = None

	return render(request, 'game/orders.html', { "game": game, "orders": all_orders})
