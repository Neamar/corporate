# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render as django_render
from django.http import Http404

from website.forms import UserCreationForm
from website.decorators import render
from django.db.models import Count
from engine.models import Game, GameForm


@render('index.html')
def index(request):
	"""
	Welcome to the Corporate Game!
	"""
	# On récupère le game id si on l'a en session pour accéder aux onglets de la session en cours
	gameid = None
	try:
		gameid = request.session['gameid']
	except:
		pass

	players = []

	if request.user.is_authenticated():
		players = request.user.player_set.all().select_related('game')

	return {
		"is_authenticated": request.user.is_authenticated(),
		"user": request.user,
		"players": players,
		"gameid": gameid,
		"request": request,
	}


@render('join_game.html')
def join_game(request):
	"""
	Join a game
	"""
	# On récupère le game id si on l'a en session pour accéder aux onglets de la session en cours
	gameid = None
	try:
		gameid = request.session['gameid']
	except:
		pass

	games = []
	MAX_PLAYER = 8

	if request.user.is_authenticated():
		# We get every game that is not started and with a number of players < max players
		games = Game.objects.exclude(player__user=request.user).filter(status='created').annotate(num_player=Count('player')).filter(num_player__lte=MAX_PLAYER)

	return {
		"is_authenticated": request.user.is_authenticated(),
		"user": request.user,
		"games": games,
		"gameid": gameid,
		"request": request,
	}


@render('create_game.html')
def create_game(request):
	"""
	Create a game
	"""
	if not request.user.is_authenticated():
		raise Http404("You need to be logged in to create a game")

	if request.method == 'POST':
		form = GameForm(request.POST)
		if form.is_valid():
			# We add the user and the game (they are not in the form)
			game = form.save(commit=False)
			game.owner = request.user
			game.save()
			return redirect('website.views.data.add_player', game_id=game.pk)
	else:
		# creation form
		form = GameForm()

	return django_render(request, 'create_game.html', {
		"form": form,
		"request": request,
	})


@render('signup.html')
@transaction.atomic
def signup(request):
	"""
	Signup page, for new users.
	"""

	if request.user.is_authenticated():
		return redirect('website.views.index.index')

	if request.POST:
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user = authenticate(username=request.POST.get('username'), password=request.POST.get('password1'))
			login(request, user)

			return redirect('website.views.index.index')
	else:
		form = UserCreationForm()

	return {
		"form": form
	}
