from django.http import Http404

from engine.exceptions import OrderNotAvailable
from engine.models import Player
from engine.modules import orders_list


def get_player(request, game_id):
	"""
	Retrieve a player associated with the user and the game.
	Returns 404 exception if the user has no access to this game, or the game does not exists.
	"""
	try:
		return Player.objects.select_related('game').get(user=request.user, game=game_id)
	except:
		raise Http404("You have no access to this game.")


def get_order_by_name(order_name):
	"""
	Return the class with the name specified.
	Will raise ValueError when Order does not exists.
	"""
	all_orders_dict = {Order.__name__: Order for Order in orders_list}
	return all_orders_dict[order_name]


def get_orders_availability(player):
	"""
	Return an array holding all orders availability.
	Each item consists of a dict as defined in get_order_availability
	"""
	orders_availability = [get_order_availability(Order, player) for Order in orders_list]

	# Sort by ORDER
	orders_availability = sorted(orders_availability, key=lambda oa: oa['type'].ORDER)

	return orders_availability


def get_order_availability(Order, player):
	"""
	Returns a dict holding order availability status

	{
		"type": order_class,
		"name": order_class_name_string
		"available": bool
		"reason": reason_not_available
		"title": order_title
		"form": ModelForm
	}
	"""
	status = {}

	status = {
		'type': Order,
		'name': Order.__name__,
		'title': Order.title,
	}
	instance = Order(player=player)
	try:
		instance.clean()
		status['available'] = True
	except OrderNotAvailable as e:
		status['available'] = False
		status['reason'] = e.message
	except:
		status['available'] = None

	if status['available'] is not False:
		status['form'] = instance.get_form()

	return status


def get_shares_count(corporation, player, shares):
	"""
	Retrieve the number of shares owned by player in corporation
	"""

	return len([s for s in shares if s.player_id == player.pk and s.corporation == corporation])


def is_top_shareholder(corporation, player, shares):
	"""
	Return true if player is top shareholder
	"""
	players = set([s.player for s in shares if s.corporation == corporation])

	max_share_count = 0
	is_alone = False

	for p in players:
		share_count = get_shares_count(corporation, p, shares)
		if share_count == max_share_count:
			is_alone = False
		elif share_count > max_share_count:
			max_share_count = share_count
			is_alone = True

	return is_alone and get_shares_count(corporation, player, shares) == max_share_count
