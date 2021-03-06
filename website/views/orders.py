from __future__ import absolute_import
from django.shortcuts import render as django_render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.conf import settings
from engine.models import Order
from website.utils import get_player, get_orders_availability, get_order_by_name
from website.decorators import render, inject_game_and_player_into_response, find_player_from_game_id
from utils.read_markdown import read_markdown_nullable
from django.utils.safestring import mark_safe

import json


@login_required
@render('game/orders.html')
@find_player_from_game_id
@inject_game_and_player_into_response
def orders(request, game, player):
	existing_orders = [order.to_child() for order in player.order_set.filter(turn=player.game.current_turn)]
	for existing_order in existing_orders:
		existing_order.name = existing_order.__class__.__name__

	existing_orders_cost = sum(o.get_cost() for o in existing_orders)

	available_orders = get_orders_availability(player)
	for available_order in available_orders:
		path = '%s/data/order_description/%s.md' % (settings.BASE_DIR, available_order['name'])
		contents = read_markdown_nullable(path)
		available_order['info'] = mark_safe(contents)

	return {
		"available_orders": available_orders,
		"existing_orders": existing_orders,
		"existing_orders_cost": existing_orders_cost,
		"remaining_money": player.money - existing_orders_cost,
		"pods": ['d_inc', 'current_player', 'players', ],
		"turn": game.current_turn,
		"request": request,
	}


@login_required
@find_player_from_game_id
@inject_game_and_player_into_response
def get_targets(request, game, player, stealer_corporation_id, qs=None):

	stealer_corporation = game.corporation_set.get(id=stealer_corporation_id)
	results = {'corporation': {}, 'market': {}}
	for m in stealer_corporation.corporation_markets:
		for cm in m.market.corporationmarket_set.filter(turn=game.current_turn, value__gte=m.value).exclude(corporation__id=stealer_corporation_id):
			corporation_slug = cm.corporation.base_corporation_slug
			if corporation_slug not in results['corporation'].keys():
				results['corporation'][corporation_slug] = []
			results['corporation'][corporation_slug].append((cm.market.name, cm.id))

			if cm.market.name not in results['market'].keys():
				results['market'][cm.market.name] = []
			results['market'][cm.market.name].append((corporation_slug, cm.id))

	return HttpResponse(json.dumps(results))


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
			return redirect('website.views.orders.orders', game_id=game_id)
	else:
		form = instance.get_form()

	path = '%s/data/order_description/%s.md' % (settings.BASE_DIR, SubOrder.__name__)
	order = {
		"game": player.game,
		"title": instance.title,
		"info": mark_safe(read_markdown_nullable(path)),
		"name": SubOrder.__name__,
		"form": form,
	}

	return django_render(request, 'game/add_order.html', {
		"game": player.game,
		"player": player,
		"order": order,
		"pods": ['d_inc', 'current_player', 'players', ],
		"request": request,
		"turn": player.game.current_turn,
	})


@login_required
def delete_order(request, game_id, order_id):
	player = get_player(request, game_id)

	order = get_object_or_404(Order, pk=order_id, player=player)
	
	if not order.cancellable:
		raise Http404("Cet ordre n'est pas annulable")

	order.delete()

	return redirect('website.views.orders.orders', game_id=game_id)
