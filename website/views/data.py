from __future__ import absolute_import
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Count

from engine_modules.share.models import Share
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory
from engine.models import Player
from website.decorators import render, find_player_from_game_id, inject_game_into_response, turn_by_turn_view
from website.utils import get_shares_count, is_top_shareholder
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
	corporations = game.get_ladder(turn=turn)
	delta_categories = {}

	assets = AssetHistory.objects.filter(corporation__game=game, turn=turn)
	assets_hash = {ah.corporation_id: ah.assets for ah in assets}

	for corporation in corporations:
		corporation.current_assets = assets_hash[corporation.pk]

	# Insert last turn assets
	last_assets = AssetHistory.objects.filter(corporation__game=game, turn=turn - 1)
	last_assets_hash = {ah.corporation_id: ah.assets for ah in last_assets}

	if game.current_turn > 1:
		for corporation in corporations:
			corporation.last_assets = last_assets_hash[corporation.pk]

			detailed_delta = corporation.assetdelta_set.filter(turn=turn).order_by('category')
			for detail in detailed_delta:
				setattr(corporation, detail.category, getattr(corporation, detail.category, 0) + detail.delta)
				delta_categories[detail.category] = detail.get_category_display()

			unknown = corporation.current_assets - corporation.last_assets - sum([ad.delta for ad in detailed_delta])
			setattr(corporation, 'unknown', unknown if unknown != 0 else "")
		delta_categories['unknown'] = '?'

	# Graph data
	sorted_corporations = sorted(corporations, key=lambda c: c.base_corporation_slug)
	assets_history = AssetHistory.objects.filter(corporation__game=game, turn__lte=turn).order_by('turn', 'corporation')

	return {
		"corporations": corporations,
		"assets_history": assets_history,
		"sorted_corporations": sorted_corporations,
		"delta_categories": OrderedDict(sorted(delta_categories.items())),
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
@turn_by_turn_view
def players(request, game, player, turn):
	"""
	Players data
	"""

	players = game.player_set.all().select_related('citizenship__corporation', 'influence').order_by('pk')
	corporations = list(game.corporation_set.all().order_by('pk'))
	shares = Share.objects.filter(player__game=game, turn=turn).select_related('corporation', 'player')
	corporations_shares = []
	totals = []
	for player in players:
		total = 0
		for corporation in corporations:
			total += get_shares_count(corporation, player, shares)
		totals.append({'player': player, 'total': total})
	for corporation in corporations:
		corporation_shares = {
			"corporation": corporation,
			"shares": [{"count": get_shares_count(corporation, player, shares), "top": is_top_shareholder(corporation, player, shares)} for player in players]
		}
		corporations_shares.append(corporation_shares)
	return {
		"totals": totals,
		"corporations": corporations,
		"corporations_shares": corporations_shares,
	}


@login_required
@render('game/player.html')
@find_player_from_game_id
@inject_game_into_response
@turn_by_turn_view
def player(request, game, player, player_id, turn):
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
