# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.shortcuts import render as django_render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Count, Case, When, IntegerField
from django.http import Http404, HttpResponseRedirect

from utils.read_markdown import parse_markdown
from engine.models import Player, PlayerForm, Game
from engine_modules.corporation.models import Corporation
from engine_modules.player_points.models import PlayerPoints
from engine_modules.share.models import Share
from player_messages.models import Message, MessageForm
from website.utils import get_shares_count, is_top_shareholder, is_citizen, get_current_money
from website.decorators import render, find_player_from_game_id, inject_game_and_player_into_response, turn_by_turn_view
from logs.models import Log, ConcernedPlayer

import json


@login_required
@render('game/add_player.html')
def add_player(request, game_id):
	"""
	Join the game by adding a player
	"""
	# if gameid is not null, we display the menu.
	# We dont want to display the menu for creation but we want to display it for modification.
	game = Game.objects.get(pk=game_id)

	# If playeryer exists we will change it, else it's a creation
	try:
		player = Player.objects.select_related('game').get(user=request.user, game=game_id)
	except:
		player = None

	if request.method == 'POST':
		form = PlayerForm(request.POST, request.FILES, instance=player, game=game)
		if form.is_valid():
			# We add the user and the game (they are not in the form)
			player = form.save(commit=False)
			player.user = request.user
			player.game = game
			player.save()
			form.save_m2m()
			return redirect('website.views.data.wallstreet', game_id=game_id)
	else:
		if player is None:
			# creation form
			form = PlayerForm(game=game)
			# We disable the game to hide the menu on this screen
			game = None
		else:
			# display game menu
			game = player.game
			# edit form
			form = PlayerForm(instance=player, game=game)

	return django_render(request, 'game/add_player.html', {
		"game_id": game_id,
		"form": form,
		"game": game,
		"request": request,
		"player": player
	})


@login_required
@render('game/wallstreet.html')
@find_player_from_game_id
@inject_game_and_player_into_response
@turn_by_turn_view
def wallstreet(request, game, player, turn):
	"""
	Wallstreet data
	"""
	# Set the game_id in session to always display all tabs
	request.session['gameid'] = game.pk

	ranking = []
	# Table data
	corporations = game.get_ladder(turn=turn - 1)
	for corporation in corporations:
		corporation_markets = corporation.get_corporation_markets(turn - 1).order_by('market__name').select_related('market')
		events = Log.objects.for_corporation(corporation, player, turn)
		if turn == game.current_turn:
			assets = corporation.assets
		else:
			assets = 0
			for market in corporation_markets:
				assets += market.value + market.bubble_value
		delta = 0
		for event_delta in Log.objects.for_delta(corporation, turn):
			delta += event_delta.delta

		events = Log.objects.for_corporation(corporation, player, turn).exclude(delta=0)
		ranking.append({"corporation": corporation, "assets": assets, "delta": delta, "corporation_market": corporation_markets, "events": events})

	return {
		"ranking": ranking,
		"pods": ['turn_spinner', 'd_inc', 'current_player', 'players', ],
		"turn": turn,
		"corporations": corporations,
		"request": request,
	}


@login_required
@render('game/game_panel.html')
@find_player_from_game_id
@inject_game_and_player_into_response
@turn_by_turn_view
def game_panel(request, game, player, turn):
	"""
	Game panel to resolve turn and start the game
	"""

	# If you are not the owner, you have nothing to do here
	# if game.owner != request.user:
	# raise Http404("Only the owner of a game can manage the game")

	# Set the game_id in session to always display all tabs
	request.session['gameid'] = game.pk

	if game.ended:
		ranking = PlayerPoints.objects.filter(player__game=game, turn=turn).order_by('-total_points')
		for pp in ranking:
			if pp.total_points == ranking[0].total_ponts:
				pp.win = True
			else:
				pp.win = False
		players = game.player_set.all()
	else:
		ranking = None
		players = game.player_set.all().annotate(
				numordre=Count(Case(
					When(order__turn=game.current_turn, then=1),
					delfault=0,
					output_field=IntegerField(),
				))
			).filter(numordre=0)

		if(request.GET.get('resolve_turn')):
			game.resolve_current_turn()

		if(request.GET.get('start_game')):
			game.start_game()

		if(request.GET.get('end_game')):
			game.end_game()

	return django_render(request, 'game/game_panel.html', {
		"game": game,
		"request": request,
		"players": players,
		"pods": ['d_inc', 'current_player', 'players', ],
		"turn": game.current_turn,
		"player": player,
		"ranking":ranking,
	})


@login_required
@render('game/discussion.html')
@find_player_from_game_id
@inject_game_and_player_into_response
def discussion(request, game, player, sender_id):
	"""
	Panel to show discussions with other players
	"""
	# Set the game_id in session to always display all tabs
	request.session['gameid'] = game.pk

	sender = Player.objects.get(pk=sender_id)

	if request.method == 'POST':
		if player.game != sender.game:
			raise Http404("Seul les joueurs appartenant à la même partie peuvent discuter entre eux")
		form = MessageForm(request.POST)
		if form.is_valid():
			# We add the sender and the receiver (they are not in the form)
			message = form.save(commit=False)
			message.sender = player
			message.receiver = sender
			message.save()
			return HttpResponseRedirect('')
	else:
		# creation form
		form = MessageForm()

	messages = Message.objects.get_discussion(player, sender)

	return django_render(request, 'game/discussion.html', {
		"game": game,
		"sender": sender,
		"messages": messages,
		"form": form,
		"request": request,
	})


@login_required
@render('game/corporation.html')
@find_player_from_game_id
@inject_game_and_player_into_response
@turn_by_turn_view
def corporation(request, player, game, corporation_slug, turn):
	"""
	Corporation data
	"""
	# Set the game_id in session to always display all tabs
	request.session['gameid'] = game.pk

	corporation = Corporation.objects.get(base_corporation_slug=corporation_slug, game_id=game.pk)
	share_holders = game.player_set.filter(game_id=game.pk, share__corporation=corporation).annotate(qty_share=Count('share')).order_by('-qty_share')
	previous_corporation_markets = corporation.get_corporation_markets(turn=turn - 1)
	current_markets = corporation.markets
	competitors = game.corporation_set.filter(corporationmarket__market__in=current_markets).distinct().order_by('base_corporation_slug')

	summary = []
	for corpo in competitors:
		assets = []
		holders = game.player_set.filter(share__corporation__base_corporation_slug=corpo.base_corporation_slug).distinct()
		corporation_markets = corpo.corporationmarket_set.filter(market__in=current_markets, turn=turn - 1)
		for market in current_markets:
			assets.append(next((cm.value for cm in corporation_markets if cm.market.name == market.name), None))

		summary.append({
			"corporation": corpo,
			"assets": assets,
			"holders": holders
		})

	assets_history = corporation.assethistory_set.all()

	for corporation_market in previous_corporation_markets:
		corporation_market.events = Log.objects.for_corporation_market(corporation_market, player)

	logs = Log.objects.for_corporation(corporation, asking_player=player, turn=turn).filter(delta=0)

	return {
		"corporation": corporation,
		"share_holders": share_holders,
		"assets_history": assets_history,
		"markets": current_markets,
		"corporation_markets": previous_corporation_markets,
		"summary": summary,
		# Turn_spinner doesn't work, because the URL with e turn isn't allowed, which makes sense, because for this description, the turn doesn't matter
		"pods": ['d_inc', 'current_player', 'players', ],
		"turn": game.current_turn,
		"logs": logs,
		"request": request,
	}


@login_required
@render('game/shares.html')
@find_player_from_game_id
@inject_game_and_player_into_response
@turn_by_turn_view
def shares(request, game, player, turn):
	"""
	Shares data
	"""
	# Set the game_id in session to always display all tabs
	request.session['gameid'] = game.pk

	players = game.player_set.all().order_by('name')
	corporations = list(game.get_ladder(turn=turn - 1))
	shares = Share.objects.filter(player__game=game, turn__lte=turn - 1).select_related('corporation', 'player')
	corporations_shares = []
	totals = []
	for player in players:
		total = 0
		for corporation in corporations:
			total += get_shares_count(corporation, player, shares)
		totals.append(total)
	for corporation in corporations:
		assets = corporation.assethistory_set.get(turn=turn - 1).assets

		corporation_shares = {
			"corporation": corporation,
			"assets": assets,
			"shares": [{"count": get_shares_count(corporation, player, shares), "top": is_top_shareholder(corporation, player, shares), "citizen": is_citizen(corporation, player)} for player in players]
		}
		corporations_shares.append(corporation_shares)
	players = game.player_set.all().annotate(Count('share')).select_related('user').order_by('name')

	return {
		"totals": totals,
		"players": players,
		"corporations": corporations,
		"corporations_shares": corporations_shares,
		"pods": ['turn_spinner', 'd_inc', 'current_player', 'players', ],
		"turn": turn,
		"request": request,
	}


@login_required
@render('game/player.html')
@find_player_from_game_id
@inject_game_and_player_into_response
@turn_by_turn_view
def player(request, player, game, player_id, turn):
	"""
	Player data
	"""

	# Set the game_id in session to always display all tabs
	request.session['gameid'] = game.pk

	player_profile = Player.objects.get(pk=player_id, game_id=game.pk)
	corporations = Corporation.objects.filter(game=player.game, share__player=player_profile).annotate(qty_share=Count('share')).order_by('-qty_share')

	rp, _ = parse_markdown(player_profile.rp)
	rp = mark_safe(rp)

	events = Log.objects.for_player(player=player_profile, asking_player=player, turn=turn)

	if player == player_profile:
		money = unicode(get_current_money(player_profile, turn)) + u" k"
		help_text_money = u"Argent disponible"
	else:
		# The money is supposed to be a personal information.
		# If you have used a information  operation to get the money next turn on a player you are supposed to see it
		# But only the money at start of the turn, not the money left on player right now
		help_text_money = u"Argent disponible pour le tour"
		# We have to find a log that is linked to both players
		concernedPlayer = ConcernedPlayer.objects.filter(log__event_type=game.MONEY_NEXT_TURN, log__game=game, log__turn=turn - 1).order_by('log')
		is_target = False
		is_spy = False
		last_log = None
		for m2m in concernedPlayer:
			if last_log != m2m.log:
				is_target = False
				is_spy = False
				last_log = m2m.log
			if m2m.player == player:
				is_spy = True
			if m2m.player == player_profile and m2m.personal:
				is_target = True
			if is_target and is_spy:
				break

		if is_target and is_spy:
			data = Log.objects.filter(event_type=game.MONEY_NEXT_TURN, game=game, turn=turn - 1, concernedplayer__player=player_profile, concernedplayer__personal=True)[0].data
			context = json.loads(data)
			money = unicode(context['money']) + u" k"
		else:
			money = '?'

	# We do not display the background as long as the viewer doesn't used an information opération to see it
	# The targeted player is saved in database as a string in the data field which is a json serialized
	# We will rebuild the piece of string we need and find if it exists in the string stored in database
	piece_of_string = u'"player_id": ' + unicode(player_profile.id)
	if player == player_profile or Log.objects.filter(event_type=game.BACKGROUND, game=game, data__contains=piece_of_string, concernedplayer__player=player).count() > 0:
		background = player_profile.background
	else:
		background = u"Vous devez lancer une opération d'information contre ce joueur pour connaitre son background"

	return {
		"player_profile": player_profile,
		"money": money,
		"rp": rp,
		"corporations": corporations,
		"qty_shares": sum([corporation.qty_share for corporation in corporations]),
		"events": events,
		"request": request,
		"citizenship": player_profile.citizenship.corporation,
		"pods": ['d_inc', 'current_player', 'players', ],
		"turn": game.current_turn,
		"background": background,
		"help_text_money": help_text_money,
	}
