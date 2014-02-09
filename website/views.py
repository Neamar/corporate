from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from website.utils import get_player, get_orders_availability, get_order_by_name


def index(request):
	return render(request, 'index.html', {})


@login_required
def orders(request, game_id):
	player = get_player(request, game_id)

	all_orders = get_orders_availability(player)

	return render(request, 'game/orders.html', {"game": player.game, "orders": all_orders})


@login_required
def add_order(request, game_id, order_type):
	player = get_player(request, game_id)

	# Retrieve OrderClass
	try:
		Order = get_order_by_name(order_type)
	except ValueError:
		raise Http404("This is not an Order.")

	instance = Order(player=player)

	if request.method == 'POST':
		form = instance.get_form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('website.views.orders', game_id=game_id)
	else:
		form = instance.get_form()

	order = {
		"title": instance.title,
		"name": Order.__name__,
		"form": form
	}

	return render(request, 'game/add_order.html', {"game": player.game, "order": order})


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
