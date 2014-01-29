from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from engine.modules import orders_list
from engine.exceptions import OrderNotAvailable
from website.utils import get_game, get_player


def index(request):
	return render(request, 'index.html', {})


@login_required
def orders(request, game_id):
	player = get_player(request, game_id)
	game = get_game(request, game_id)

	all_orders = [{"type": order, 'name': order.__name__} for order in orders_list]

	for order in all_orders:
		instance = order["type"](player=player)
		try:
			instance.clean()
			order['available'] = True
		except OrderNotAvailable:
			order['available'] = False
		except:
			order['available'] = None
		
		order['title'] = instance.title
		if order['available'] != False:
			order['form'] = instance.get_form()

	return render(request, 'game/orders.html', { "game": game, "orders": all_orders})


@login_required
def add_order(request, game_id):
	player = get_player(request, game_id)
	game = get_game(request, game_id)

	return render(request, 'game/orders.html', { "game": game, "orders": all_orders})
