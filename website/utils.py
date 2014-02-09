from django.shortcuts import get_object_or_404

from engine.exceptions import OrderNotAvailable
from engine.models import Player
from engine.modules import orders_list


def get_player(request, game_id):
	"""
	Retrieve a player associated with the user and the game.
	Returns 404 exception if the user has no access to this game, or the game does not exists.
	"""
	return get_object_or_404(Player, user=request.user, game=game_id)


def get_orders_availability(player):
	"""
	Return an array holding all orders availability.
	Each item consists of a dict as defined in get_order_availability
	"""
	orders_availability = [get_order_availability(Order, player) for Order in orders_list]

	return orders_availability


def get_order_availability(Order, player):
	"""
	Returns a dict holding order availability status

	{
		"type": order_class,
		"name": order_class_name_string
		"available": bool
		"title": order_title
		"form": ModelForm
	}
	"""
	status = {}

	status = {
		'type': Order,
		'name': Order.__name__
	}
	instance = Order(player=player)
	try:
		instance.clean()
		status['available'] = True
	except OrderNotAvailable:
		status['available'] = False
	except:
		status['available'] = None
	
	status['title'] = instance.title
	if status['available'] is not False:
		status['form'] = instance.get_form()

	return status
