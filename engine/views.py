from django.shortcuts import render

from engine.models import Game
from engine.modules import __orders_list

def index(request, game_id):
	orders = __orders_list
	return render(request, 'game/index.html', {"orders": orders})


def players(request, game_id):
	g = Game.objects.get(pk=game_id)
	return render(request, 'game/players.html', {"players": g.player_set.all()})
