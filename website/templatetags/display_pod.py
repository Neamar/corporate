# -*- coding: utf-8 -*-
from django import template
from django.template.loader import get_template
from logs.models import Log
from django.conf import settings

from engine_modules.detroit_inc.models import DIncVoteOrder

import re
import string

register = template.Library()

NO_CONTEXT_REQUIRED = "__no_context"


def players_pod(context):
	players = context['game'].player_set.all()

	for player in players:
		player.events = Log.objects.for_player(player=player, asking_player=context['player'], turn=context['turn'])
	return {
		'players': players
	}


def d_inc_pod_hover(session, orders):

	votes_details = {}

	# Build global dict
	coalition_breakdown = []
	for order in orders:
		if(order.coalition not in votes_details):
			votes_details[order.coalition] = {
				"display": order.get_coalition_display(),
				"members": [],
				"count": 0
			}
		votes_details[order.coalition]["members"].append({
			'player':
			order.player,
			'corporations': order.get_friendly_corporations(),
		})
		votes_details[order.coalition]["count"] += order.get_weight()

	for vote in votes_details.values():
		coalition = vote["display"]
		count = vote["count"]

		siders = []
		for member in vote["members"]:
			member_string = unicode(member['player'])
			if len(member['corporations']) > 0:
				member_string += " (%s)" % (", ".join(unicode(c.base_corporation.name) for c in member['corporations']))
			siders.append(member_string)

		siders = " ".join(["<li>%s" % s for s in siders])

		content = u"<strong>%s</strong> a reçu <strong>%s</strong> voix : <ul>%s</ul>" % (coalition, count, siders)

		coalition_breakdown.append(content)

	return coalition_breakdown


def d_inc_pod(context):

	game = context['game']
	current_coalition = game.get_dinc_coalition(turn=context['turn'])
	orders = DIncVoteOrder.objects.filter(player__game=game, turn=game.current_turn - 1)

	if current_coalition is None:
		current_coalition = 'None'
		display = 'Aucune coalition n''a obtenu la majoritée ce tour-ci.'
	else:
		display = string.join(d_inc_pod_hover(current_coalition, orders), '')
	return {
		'd_inc_line': current_coalition,
		'd_inc_line_display': display
	}


def current_player_pod(context):
	existing_orders = [order.to_child() for order in context['player'].order_set.filter(turn=context['turn'])]
	existing_orders_cost = sum(o.cost for o in existing_orders)

	money_left = context['player'].money - existing_orders_cost

	return {
		'ic': context['player'].get_influence(turn=context['turn']).level,
		'money': money_left,
		'display_turn': context['turn'],
	}


def turn_spinner_pod(context):
	return {
		'game': context['game'],
		'display_turn': context['turn'],
		'total_turns': range(1, 8, 1),
	}


def corporation_documentation(context):
	return {
		"base_corporations": context['base_corporations'],
		NO_CONTEXT_REQUIRED: True
	}


# Map string name to pod generator
pods_functions = {
	"players": players_pod,
	"d_inc": d_inc_pod,
	"current_player": current_player_pod,
	"turn_spinner": turn_spinner_pod,
	"corporation_documentation": corporation_documentation
}


@register.simple_tag(takes_context=True, name="display_pod")
def display_pod(context, pod, *args, **kwargs):
	template = get_template('pods/' + pod + '.html')

	pod_context = pods_functions[pod](context)
	if NO_CONTEXT_REQUIRED not in pod_context:
		pod_context['game'] = context['game']
		pod_context['player'] = context['player']
		pod_context['turn"'] = context['turn']

		# does not work when using URL like game/1/wallstreet, because the turn is default, not explicit
		path_list = context['request'].path.split('/')
		path_len = len(path_list)
		# remove turn number if there was one
		if len(re.findall('\d+', path_list[-1])) != 0:
			path_len -= 1

		pod_context['request_path'] = ''.join(s + '/' for s in path_list[:path_len])
		pod_context['STATIC_URL'] = settings.STATIC_URL

	return template.render(pod_context)
