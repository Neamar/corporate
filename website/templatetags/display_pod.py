from django import template
from django.template.loader import get_template

register = template.Library()


def players_pod(context):
	return {}


def d_inc_pod(context):
	return {
		'd_inc_line': 'CONS',
		'd_inc_line_display': 'Consolidation'
	}


def current_player_pod(context):
	return {}


def turn_spinner_pod(context):
	return {}


# Map string name to pod generator
pods_functions = {
	"players": players_pod,
	"d_inc": d_inc_pod,
	"current_player": current_player_pod,
	"turn_spinner": turn_spinner_pod,
}


@register.simple_tag(takes_context=True, name="display_pod")
def display_pod(context, pod, *args, **kwargs):
	template = get_template('pods/' + pod + '.html')

	pod_context = pods_functions[pod](context)
	pod_context['game'] = context['game']
	pod_context['player'] = context['player']

	return template.render(pod_context)
