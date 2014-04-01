from __future__ import absolute_import

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Count

from engine_modules.corporation.models import Corporation, AssetDelta
from engine_modules.corporation_asset_history.models import AssetHistory
from engine_modules.share.models import Share
from engine.models import Player
from website.utils import get_player, get_shares_count
from utils.read_markdown import parse_markdown


@login_required
def wallstreet(request, game_id):
	"""
	Wallstreet datas
	"""
	player = get_player(request, game_id)
	game = player.game

	# Table datas
	corporations = game.get_ladder()
	if game.current_turn > 1:
		# Insert last turn assets
		delta = AssetHistory.objects.filter(corporation__game=game, turn=game.current_turn - 2)
		delta_hash = {ah.corporation_id: ah.assets for ah in delta}

		delta_categories = set([])
		for corporation in corporations:
			corporation.last_assets = delta_hash[corporation.pk]
			detailed_delta = corporation.assetdelta_set.filter(turn=game.current_turn - 2)
			for detail in detailed_delta:
				setattr(corporation, detail.category, getattr(corporation, detail.category, 0) + detail.delta)
				delta_categories.add(detail.category)
		print delta_categories

	# Graph datas
	sorted_corporations = sorted(corporations, key=lambda c: c.base_corporation_slug)
	assets_history = AssetHistory.objects.filter(corporation__game=game).order_by('turn', 'corporation')

	# Derivatives
	derivatives = game.derivative_set.all()
	for derivative in derivatives:
		derivative.assets = derivative.get_sum(game.current_turn - 1)
		derivative.last_assets = derivative.get_sum(game.current_turn - 2)

	return render(request, 'game/wallstreet.html', {
		"corporations": corporations,
		"assets_history": assets_history,
		"sorted_corporations": sorted_corporations,
		"derivatives": derivatives,
		"delta_categories": delta_categories
	})


@login_required
def corporations(request, game_id):
	"""
	corporations datas
	"""
	player = get_player(request, game_id)
	corporations = player.game.corporation_set.all()
	return render(request, 'game/corporations.html', {
		"corporations": corporations
	})


@login_required
def corporation(request, game_id, corporation_slug):
	"""
	Corporation datas
	"""
	corporation = Corporation.objects.get(base_corporation_slug=corporation_slug, game_id=game_id)
	players = Player.objects.filter(game_id=game_id, share__corporation=corporation).annotate(qty_share=Count('share')).order_by('-qty_share')
	players = players.select_related('citizenship')

	assets_history = corporation.assethistory_set.all()
	return render(request, 'game/corporation.html', {
		"corporation": corporation,
		"players": players,
		"assets_history": assets_history
	})


@login_required
def players(request, game_id):
	"""
	Players datas
	"""
	player = get_player(request, game_id)
	game = player.game

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

	return render(request, 'game/players.html', {
		"players": players,
		"corporations": corporations,
		"shares": player_shares
	})


@login_required
def player(request, game_id, player_id):
	"""
	Player datas
	"""
	player = Player.objects.select_related('influence', 'citizenship__corporation').get(pk=player_id, game_id=game_id)
	corporations = Corporation.objects.filter(game=player.game, share__player=player).annotate(qty_share=Count('share')).order_by('-qty_share')

	return render(request, 'game/player.html', {
		"player": player,
		"corporations": corporations
	})


@login_required
def shares(request, game_id):
	"""
	Shares datas
	"""
	player = get_player(request, game_id)
	game = player.game

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

	return render(request, 'game/shares.html', {
		"corporations": corporations,
		"shares": player_shares
	})


@login_required
def newsfeeds(request, game_id, turn=None):
	"""
	Display newsfeed
	"""
	player = get_player(request, game_id)

	if turn is None:
		turn = player.game.current_turn - 1
	turn = int(turn)

	if turn >= player.game.current_turn:
		return redirect('website.views.datas.newsfeeds', game_id=game_id)

	newsfeeds = player.game.newsfeed_set.filter(turn=turn).order_by('category')

	return render(request, 'game/newsfeeds.html', {
		"newsfeeds": newsfeeds,
		"current_turn": turn,
		"turns": range(1, player.game.current_turn)
	})


@login_required
def comlink(request, game_id):
	"""
	Display comlink
	"""
	player = get_player(request, game_id)

	messages = player.message_set.all().order_by("-turn", "-pk")

	return render(request, 'game/comlink.html', {
		"messages": messages
	})


@login_required
def message(request, game_id, message_id):
	"""
	Display message
	"""
	player = get_player(request, game_id)

	message = player.message_set.get(pk=message_id)

	message.html, _ = parse_markdown(message.content)
	message.html = mark_safe(message.html)

	return render(request, 'game/message.html', {
		"message": message
	})
