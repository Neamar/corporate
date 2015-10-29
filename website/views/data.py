from __future__ import absolute_import
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Count

from engine_modules.corporation.models import Corporation
from website.decorators import render, find_player_from_game_id, inject_game_and_player_into_response, turn_by_turn_view
from engine.models import Player
from engine_modules.share.models import Share
from website.utils import get_shares_count, is_top_shareholder
from utils.read_markdown import parse_markdown
from logs.models import Log


@login_required
@render('game/wallstreet.html')
@find_player_from_game_id
@inject_game_and_player_into_response
@turn_by_turn_view
def wallstreet(request, game, player, turn):
	"""
	Wallstreet data
	"""

	ranking = []
	# Table data
	corporations = game.get_ladder(turn=turn - 1)
	for corporation in corporations:
		corporation_markets = corporation.get_corporation_markets(turn - 1).order_by('market__name')
		events = Log.objects.for_corporation(corporation, player, turn).exclude(delta=0)
		ranking.append({"corporation": corporation, "corporation_market": corporation_markets, "events": events})

	return {
		"ranking": ranking,
		"pods": ['turn_spinner', 'd_inc', 'current_player', 'players', ],
		"turn": turn,
		"corporations": corporations,
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

	events = Log.objects.for_player(player=player_profile, asking_player=player, turn=turn)

	return {
		"player_profile": player_profile,
		"rp": rp,
		"corporations": corporations,
		"qty_shares": sum([corporation.qty_share for corporation in corporations]),
		"events": events,
		"request": request,
	}
