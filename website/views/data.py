from __future__ import absolute_import
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Count

from engine_modules.corporation.models import Corporation
from engine.models import Player
from engine_modules.share.models import Share
from website.utils import get_shares_count, is_top_shareholder
from website.decorators import render, find_player_from_game_id, inject_game_into_response, turn_by_turn_view
from utils.read_markdown import parse_markdown


@login_required
@render('game/wallstreet.html')
@find_player_from_game_id
@inject_game_into_response
@turn_by_turn_view
def wallstreet(request, game, player, turn):
	"""
	Wallstreet data
	"""

	# Table data
	ranking = []
	corporations = game.get_ladder(turn=turn - 1)
	for corporation in corporations:
		corporation_markets = corporation.get_corporation_markets(turn - 1).order_by('market__name')
		ranking.append((corporation, corporation_markets))

	return {
		"corporations": corporations
	}


@login_required
@render('game/corporation.html')
@find_player_from_game_id
@inject_game_into_response
def corporation(request, player, game, corporation_slug):
	"""
	Corporation data
	"""
	corporation = Corporation.objects.get(base_corporation_slug=corporation_slug, game_id=game.pk)
	players = Player.objects.filter(game_id=game.pk, share__corporation=corporation).annotate(qty_share=Count('share')).order_by('-qty_share')

	assets_history = corporation.assethistory_set.all()
	return {
		"corporation": corporation,
		"players": players,
		"assets_history": assets_history
	}


@login_required
@render('game/players.html')
@find_player_from_game_id
@inject_game_into_response
def players(request, game, player):
	"""
	Players data
	"""

	players = game.player_set.all().annotate(Count('share')).select_related('user').order_by('name')

	return {
		"players": players,
	}


@login_required
@render('game/player.html')
@find_player_from_game_id
@inject_game_into_response
def player(request, game, player, player_id):
	"""
	Player data
	"""
	player = Player.objects.get(pk=player_id, game_id=game.pk)
	corporations = Corporation.objects.filter(game=player.game, share__player=player).annotate(qty_share=Count('share')).order_by('-qty_share')

	rp, _ = parse_markdown(player.rp)
	rp = mark_safe(rp)

	return {
		"player": player,
		"rp": rp,
		"corporations": corporations
	}


@login_required
@render('game/shares.html')
@find_player_from_game_id
@inject_game_into_response
@turn_by_turn_view
def shares(request, game, player, turn):
	"""
	Shares data
	"""

	players = game.player_set.all().order_by('pk')
	corporations = list(game.corporation_set.all().order_by('pk'))
	shares = Share.objects.filter(player__game=game, turn__lte=turn).select_related('corporation', 'player')
	player_shares = []

	for player in players:
		player_share = {
			"player": player,
			"shares": [{"count": get_shares_count(c, player, shares), "top": is_top_shareholder(c, player, shares)} for c in corporations]
		}

		try:
			player_share["citizenship_index"] = corporations.index(player.citizenship.corporation)
		except ValueError:
			pass

		player_shares.append(player_share)

	return {
		"corporations": corporations,
		"shares": player_shares
	}


@login_required
@render('game/newsfeeds.html')
@find_player_from_game_id
@inject_game_into_response
@turn_by_turn_view
def newsfeeds(request, game, player, turn):
	"""
	Display newsfeed
	"""

	newsfeeds = game.newsfeed_set.filter(turn=turn, path="").order_by('category')
	newsfeeds_rp = game.newsfeed_set.filter(turn=turn).exclude(path="").order_by('category')

	return {
		"newsfeeds": newsfeeds,
		"newsfeeds_rp": newsfeeds_rp,
	}


@login_required
@render('game/comlink.html')
@find_player_from_game_id
@inject_game_into_response
def comlink(request, game, player):
	"""
	Display comlink
	"""

	messages = player.message_set.all().order_by("-turn", "-pk")

	return {
		"messages": messages
	}


@login_required
@render('game/message.html')
@find_player_from_game_id
@inject_game_into_response
def message(request, game, player, message_id):
	"""
	Display message
	"""

	message = player.message_set.get(pk=message_id)

	message.html, _ = parse_markdown(message.content)
	message.html = mark_safe(message.html)

	return {
		"message": message
	}
