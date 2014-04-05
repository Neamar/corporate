from __future__ import absolute_import
from collections import OrderedDict
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Count

from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory
from engine_modules.share.models import Share
from engine.models import Player
from website.utils import get_player, get_shares_count
from website.decorators import render, find_player_from_game_id
from utils.read_markdown import parse_markdown


@login_required
@render('game/wallstreet.html')
@find_player_from_game_id
def wallstreet(request, game, player):
	"""
	Wallstreet datas
	"""

	# Table datas
	corporations = game.get_ladder()
	delta_categories = OrderedDict()

	if game.current_turn > 1:
		# Insert last turn assets
		delta = AssetHistory.objects.filter(corporation__game=game, turn=game.current_turn - 2)
		delta_hash = {ah.corporation_id: ah.assets for ah in delta}

		for corporation in corporations:
			corporation.last_assets = delta_hash[corporation.pk]

			detailed_delta = corporation.assetdelta_set.filter(turn=game.current_turn - 1).order_by('category')
			for detail in detailed_delta:
				setattr(corporation, detail.category, getattr(corporation, detail.category, 0) + detail.delta)
				delta_categories[detail.category] = {
					"shortcut": detail.get_category_shortcut(),
					"display": detail.get_category_display()
				}

			unknown = corporation.assets - corporation.last_assets - sum([ad.delta for ad in detailed_delta])
			setattr(corporation, 'unknown', unknown if unknown != 0 else "")
		delta_categories['unknown'] = {
			'shortcut': '?',
			'display': 'Modifications non publiques'
		}

	# Graph datas
	sorted_corporations = sorted(corporations, key=lambda c: c.base_corporation_slug)
	assets_history = AssetHistory.objects.filter(corporation__game=game).order_by('turn', 'corporation')

	# Derivatives
	derivatives = game.derivative_set.all()
	for derivative in derivatives:
		derivative.assets = derivative.get_sum(game.current_turn - 1)
		if game.current_turn > 1:
			derivative.last_assets = derivative.get_sum(game.current_turn - 2)

	return {
		"game": game,
		"corporations": corporations,
		"assets_history": assets_history,
		"sorted_corporations": sorted_corporations,
		"derivatives": derivatives,
		"delta_categories": delta_categories,
	}


@login_required
@render('game/corporations.html')
@find_player_from_game_id
def corporations(request, game, player):
	"""
	corporations datas
	"""
	corporations = game.corporation_set.all()
	return {
		"game": player.game,
		"corporations": corporations
	}


@login_required
@render('game/corporation.html')
@find_player_from_game_id
def corporation(request, player, game, corporation_slug):
	"""
	Corporation datas
	"""
	corporation = Corporation.objects.get(base_corporation_slug=corporation_slug, game_id=game.pk)
	players = Player.objects.filter(game_id=game.pk, share__corporation=corporation).annotate(qty_share=Count('share')).order_by('-qty_share')
	players = players.select_related('citizenship')

	assets_history = corporation.assethistory_set.all()
	return {
		"game": corporation.game,
		"corporation": corporation,
		"players": players,
		"assets_history": assets_history
	}


@login_required
@render('game/players.html')
@find_player_from_game_id
def players(request, game, player):
	"""
	Players datas
	"""

	players = game.player_set.all().select_related('citizenship__corporation', 'influence').order_by('name')
	corporations = list(game.corporation_set.all().order_by('pk'))
	shares = Share.objects.filter(player__game=game)
	player_shares = []

	for player in players:
		player_share = {
			"player": player,
			"shares": [get_shares_count(c, player, shares) for c in corporations]
		}

		try:
			player_share["citizenship_index"] = corporations.index(player.citizenship.corporation)
		except ValueError:
			pass

		player_shares.append(player_share)

	return {
		"game": game,
		"players": players,
		"corporations": corporations,
		"shares": player_shares
	}


@login_required
@render('game/player.html')
@find_player_from_game_id
def player(request, game, player, player_id):
	"""
	Player datas
	"""
	player = Player.objects.select_related('influence', 'citizenship__corporation').get(pk=player_id, game_id=game.pk)
	corporations = Corporation.objects.filter(game=player.game, share__player=player).annotate(qty_share=Count('share')).order_by('-qty_share')

	return {
		"game": player.game,
		"player": player,
		"corporations": corporations
	}


@login_required
@render('game/shares.html')
@find_player_from_game_id
def shares(request, game, player):
	"""
	Shares datas
	"""

	players = game.player_set.all().select_related('citizenship__corporation', 'influence').order_by('pk')
	corporations = list(game.corporation_set.all().order_by('pk'))
	shares = Share.objects.filter(player__game=game)
	player_shares = []

	for player in players:
		player_share = {
			"player": player,
			"shares": [get_shares_count(c, player, shares) for c in corporations]
		}

		try:
			player_share["citizenship_index"] = corporations.index(player.citizenship.corporation)
		except ValueError:
			pass

		player_shares.append(player_share)

	return {
		"game": game,
		"corporations": corporations,
		"shares": player_shares
	}


@login_required
@render('game/newsfeeds.html')
@find_player_from_game_id
def newsfeeds(request, game, player, turn=None):
	"""
	Display newsfeed
	"""

	if turn is None:
		turn = game.current_turn - 1
	turn = int(turn)

	if turn >= game.current_turn:
		return redirect('website.views.datas.newsfeeds', game_id=game.pk)

	newsfeeds = game.newsfeed_set.filter(turn=turn).order_by('category')

	return {
		"game": game,
		"newsfeeds": newsfeeds,
		"current_turn": turn,
		"turns": range(1, game.current_turn)
	}


@login_required
@render('game/comlink.html')
@find_player_from_game_id
def comlink(request, game, player):
	"""
	Display comlink
	"""

	messages = player.message_set.all().order_by("-turn", "-pk")

	return {
		"game": game,
		"messages": messages
	}


@login_required
@render('game/message.html')
@find_player_from_game_id
def message(request, game, player, message_id):
	"""
	Display message
	"""

	message = player.message_set.get(pk=message_id)

	message.html, _ = parse_markdown(message.content)
	message.html = mark_safe(message.html)

	return {
		"game": game,
		"message": message
	}
