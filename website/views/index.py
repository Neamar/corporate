from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.db import transaction

from website.forms import UserCreationForm
from website.decorators import render


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
	}


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
