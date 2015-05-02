from django import template
from django.template.loader import get_template

register = template.Library()


def get_player_pod(context):
    game = context["game"]
    player = context["player"]
    return {
        "player": player,
        "game": game
    }


pods_functions = {
    "players": get_player_pod,
}


@register.simple_tag(takes_context=True, name="get_pod")
def get_pod(context, pod, *args, **kwargs):
    template = get_template('pods/' + pod + '.html')

    return template.render(pods_functions[pod](context))
