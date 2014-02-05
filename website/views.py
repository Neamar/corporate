from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from engine.modules import orders_list
from engine.exceptions import OrderNotAvailable
from website.utils import get_player


def index(request):
	return render(request, 'index.html', {})


@login_required
def orders(request, game_id):
	player = get_player(request, game_id)

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

	return render(request, 'game/orders.html', { "game": player.game, "orders": all_orders})


@login_required
def add_order(request, game_id, order_type):
	player = get_player(request, game_id)

	# Retrieve OrderClass
	all_orders_dict = {order.__name__:order for order in orders_list}

	try:
		Order = all_orders_dict[order_type]
	except ValueError:
		raise Http404("This is not an Order.")

	order = Order(player=player)

	return render(request, 'game/orders.html', {})


@login_required
def wallstreet(request, game_id):
	"""
	Wallstreet datas
	"""	
	return render(request, 'game/wallstreet.html', {})


@login_required
def corporations(request, game_id):
	"""
	Wallstreet datas
	"""	
	return render(request, 'game/wallstreet.html', {})


@login_required
def players(request, game_id):
	"""
	Wallstreet datas
	"""	
	return render(request, 'game/wallstreet.html', {})
