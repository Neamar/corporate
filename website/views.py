from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from engine.modules import orders_list
from engine_modules.corporation.models import Corporation
from engine_modules.citizenship.models import CitizenShip
from engine_modules.share.models import Share
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
		if order['available'] is not False:
			order['form'] = instance.get_form()

	return render(request, 'game/orders.html', {"game": player.game, "orders": all_orders})


@login_required
def add_order(request, game_id, order_type):
	player = get_player(request, game_id)

	# Retrieve OrderClass
	all_orders_dict = {order.__name__: order for order in orders_list}

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
	player = get_player(request, game_id)
	corporations = player.game.corporation_set.all()
	return render(request, 'game/wallstreet.html', {"corporations": corporations})


@login_required
def corporations(request, game_id):
	"""
	corporations datas
	"""
	player = get_player(request, game_id)
	corporations = player.game.corporation_set.all()
	return render(request, 'game/corporations.html', {"corporations": corporations})


@login_required
def players(request, game_id):
	"""
	Wallstreet datas
	"""
	shares = {}
	player = get_player(request, game_id)
	players = player.game.player_set.all().order_by('pk')

	corporations = player.game.corporation_set.all().order_by('pk')
	for player in players:
		shares[player.pk] = {}
		shares[player.pk]['name'] = player.name
		corporation_index = -1 #If no citizenship, no corporation to be set in bold
		try:
			#else share in bold should be the share of the copraration where the player is citizen
			for index, item in enumerate(corporations):
				if item == CitizenShip.objects.get(player=player).corporation:
					corporation_index = index
		except:
			pass
		print corporation_index
		shares[player.pk]['citizenship']= corporation_index
		shares[player.pk]['shares'] = {}
		for corporation in corporations:
			shares[player.pk]['shares'][corporation.pk] = Share.objects.filter(player = player, corporation = corporation).count()
	return render(request, 'game/players.html', {"players": players, "corporations": corporations, "shares": shares})
