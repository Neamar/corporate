from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from engine.models import Order
from website.utils import get_player, get_orders_availability, get_order_by_name
from messaging.models import Newsfeed


def index(request):
	return render(request, 'index.html', {})


@login_required
def orders(request, game_id):
	player = get_player(request, game_id)

	existing_orders = [order.to_child() for order in player.order_set.filter(turn=player.game.current_turn)]
	existing_orders_cost = sum(o.get_cost() for o in existing_orders)

	available_orders = get_orders_availability(player)

	return render(request, 'game/orders.html', {
		"game": player.game,
		"available_orders": available_orders,
		"existing_orders": existing_orders,
		"existing_orders_cost": existing_orders_cost,
		"remaining_money": player.money - existing_orders_cost,
	})


@login_required
def add_order(request, game_id, order_type):
	player = get_player(request, game_id)

	# Retrieve OrderClass
	try:
		SubOrder = get_order_by_name(order_type)
	except ValueError:
		raise Http404("This is not an Order.")

	instance = SubOrder(player=player)

	if request.method == 'POST':
		form = instance.get_form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('website.views.orders', game_id=game_id)
	else:
		form = instance.get_form()

	order = {
		"title": instance.title,
		"name": SubOrder.__name__,
		"form": form
	}

	return render(request, 'game/add_order.html', {"game": player.game, "order": order})


@login_required
def delete_order(request, game_id, order_id):
	player = get_player(request, game_id)

	order = get_object_or_404(Order, pk=order_id, player=player)
	order.delete()

	return redirect('website.views.orders', game_id=game_id)


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


@login_required
def newsfeeds(request, game_id):
	"""
	Display newsfeed
	"""
	player = get_player(request, game_id)

	newsfeeds = player.game.newsfeed_set.filter(turn=player.game.current_turn - 1).order_by('category')

	return render(request, 'game/newsfeeds.html', {"newsfeeds": newsfeeds})


@login_required
def comlink(request, game_id):
	"""
	Display newsfeed
	"""
	player = get_player(request, game_id)

	messages = player.message_set.all().order_by("-turn")

	return render(request, 'game/comlink.html', {"messages": messages})
