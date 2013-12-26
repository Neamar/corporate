from django.shortcuts import render


def index(request, game_id):
	return render(request, 'game/index.html', {})


def players(request, game_id):
	return render(request, 'game/players.html', {})
