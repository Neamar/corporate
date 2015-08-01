from django import template
from django.template.loader import get_template

from engine_modules.detroit_inc.models import DIncVoteOrder

import re

register = template.Library()


def players_pod(context):
	players = context['game'].player_set.all()
	return {
		'players': players
	}


def d_inc_pod(context):

	current_coalition = context['game'].get_dinc_coalition(turn=context['turn'])
	if current_coalition is None:
		current_coalition = 'None'
		display = 'None'
	else:
		for t in DIncVoteOrder.DINC_COALITION_CHOICES:
			if t[0] == current_coalition:
				display = t[1]
	return {
		'd_inc_line': current_coalition,
		'd_inc_line_display': display
	}


def current_player_pod(context):
	return {
		'ic': context['player'].get_influence(turn=context['turn']).level,
		'money': context['player'].money,
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
		"__no_context": True
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

	print "FOQUE", pod
	pod_context = pods_functions[pod](context)
	if "__no_context" not in pod_context:
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

	return template.render(pod_context)
