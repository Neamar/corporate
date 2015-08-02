from __future__ import absolute_import
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Count

from engine_modules.share.models import Share
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory
from engine.models import Player
from website.decorators import render, find_player_from_game_id, inject_game_and_player_into_response, turn_by_turn_view
from website.utils import get_shares_count, is_top_shareholder
from utils.read_markdown import parse_markdown


@login_required
@render('game/wallstreet.html')
@find_player_from_game_id
@inject_game_and_player_into_response
@turn_by_turn_view
def wallstreet(request, game, player, turn):
	"""
	Wallstreet data
	"""

	# Table data
	corporations = game.get_ladder(turn=turn - 1)
	delta_categories = {}

	assets = AssetHistory.objects.filter(corporation__game=game, turn=turn - 1)
	assets_hash = {ah.corporation_id: ah.assets for ah in assets}

	for corporation in corporations:
		corporation.current_assets = assets_hash[corporation.pk]

	# Insert last turn assets
	last_assets = AssetHistory.objects.filter(corporation__game=game, turn=turn - 2)
	last_assets_hash = {ah.corporation_id: ah.assets for ah in last_assets}

	for corporation in corporations:
		corporation.last_assets = last_assets_hash[corporation.pk] if turn > 1 else None

		detailed_delta = corporation.assetdelta_set.filter(turn=turn - 1).order_by('category')
		for detail in detailed_delta:
			if turn > 1:
				setattr(corporation, detail.category, getattr(corporation, detail.category, 0) + detail.delta)
				delta_categories[detail.category] = detail.get_category_display()
				unknown = corporation.current_assets - corporation.last_assets - sum([ad.delta for ad in detailed_delta])
			else:
				setattr(corporation, detail.category, None)
				unknown = None
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
		"pods": ['turn_spinner', 'd_inc', 'current_player', 'players', ],
		"turn": turn,
		"request": request,
	}


@login_required
@render('game/corporation.html')
@find_player_from_game_id
@inject_game_and_player_into_response
@turn_by_turn_view
def corporation(request, player, game, corporation_slug, turn):
	"""
	Corporation data
	"""
	corporation = Corporation.objects.get(base_corporation_slug=corporation_slug, game_id=game.pk)
	share_holders = game.player_set.filter(game_id=game.pk, share__corporation=corporation).annotate(qty_share=Count('share')).order_by('-qty_share')
	markets = corporation.markets
	competitors = game.corporation_set.filter(corporationmarket__market__in=markets).distinct().order_by('base_corporation_slug')

	summary = []
	for corpo in competitors:
		assets = []
		holders = game.player_set.filter(share__corporation__base_corporation_slug=corpo.base_corporation_slug).distinct()
		corporation_markets = corpo.corporationmarket_set.filter(market__in=markets)
		for market in markets:
			assets.append(next((cm.value for cm in corporation_markets if cm.market.name == market.name), None))
		# That's kind of a weird data structure, but the template tags are not as flexible as one might like
		summary.append((corpo, assets, holders))

	assets_history = corporation.assethistory_set.all()
	return {
		"corporation": corporation,
		"share_holders": share_holders,
		"assets_history": assets_history,
		"markets": markets,
		"summary": summary,
		# Turn_spinner doesn't work, because the URL with e turn isn't allowed, which makes sense, because for this description, the turn doesn't matter
		"pods": ['d_inc', 'current_player', 'players', ],
		"turn": game.current_turn,
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

	players = game.player_set.all().order_by('pk')
	corporations = list(game.corporation_set.all().order_by('pk'))
	shares = Share.objects.filter(player__game=game, turn__lte=turn).select_related('corporation', 'player')
	corporations_shares = []
	totals = []
	for player in players:
		total = 0
		for corporation in corporations:
			total += get_shares_count(corporation, player, shares)
		totals.append(total)
	for corporation in corporations:
		corporation_shares = {
			"corporation": corporation,
			"shares": [{"count": get_shares_count(corporation, player, shares), "top": is_top_shareholder(corporation, player, shares)} for player in players]
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

	player_profile = Player.objects.get(pk=player_id, game_id=game.pk)
	corporations = Corporation.objects.filter(game=player.game, share__player=player).annotate(qty_share=Count('share')).order_by('-qty_share')

	rp, _ = parse_markdown(player.rp)
	rp = mark_safe(rp)

	return {
		"player_profile": player_profile,
		"rp": rp,
		"corporations": corporations,
		"qty_shares": sum([corporation.qty_share for corporation in corporations]),
		"request": request,
	}
