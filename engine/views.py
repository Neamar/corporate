from django.shortcuts import render

from engine.models import Game, Player
from engine.modules import __orders_list

def index(request, game_id):
	player = Player.objects.get(game=game_id, user=request.user)

	ret = {
		"available_orders": __orders_list,
		"orders": player.get_current_orders(),
		"game": player.game,
	}
	
	return render(request, 'game/index.html', ret)


def players(request, game_id):
	g = Game.objects.get(pk=game_id)
	return render(request, 'game/players.html', {"players": g.player_set.all()})
