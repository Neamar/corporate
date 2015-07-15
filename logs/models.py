# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Game


class Logs(models.Model):
	"""
	We log every action in the game in a single table
	"""
	turn = models.PositiveSmallIntegerField()
	game = models.ForeignKey('engine.Game')

	# how much assets are lost or mon on a market
	delta = models.SmallIntegerField()

	# some icons must be duplicated for display on a corporation but not on a player
	# for example we want a +1 and a -1 icon for an extraction but just one extraction icon on the player who orders it
	# So the -1 Log is hide for players to just have one icon
	hide_for_players = models.BooleanField()

	# To avoid attaching public info on all 8 players and simplify end_game request we created a flag 'public'
	public = models.BooleanField()

	# An event_type is a type of game_event. All game_events are defined in Game
	event_type = models.CharField(max_length=30)

	# data contains a json with all the informations needed for the text.
	data = models.TextField()

	# the coporation concerned by the log
	corporation = models.ForeignKey('corporation.Corporation', null=True)

	# the corporationmarket concerned for this log
	corporationmarket = models.ForeignKey('market.CorporationMarket', null=True)

	# the orderer of the action and all the players knowing the action. Parameters are defferent between ordrer and knowers, see ConcernedPlayers
	players = models.ManyToManyField('engine.Player', through='ConcernedPlayers')

	# List of game events that are hide for players (see hide for player above)
	HIDE_FOR_PLAYERS = [
		Game.OPE_DATASTEAL_FAIL_DOWN,
		Game.OPE_DATASTEAL_DOWN,
		Game.OPE_EXTRACTION_FAIL_DOWN,
		Game.OPE_EXTRACTION_DOWN]

	# list of public game events
	PUBLIC = [
		Game.FIRST_EFFECT,
		Game.LAST_EFFECT,
		Game.CRASH_EFFECT,
		Game.EFFECT_CONTRAT_UP,
		Game.EFFECT_CONTRAT_DOWN,
		Game.ADD_CITIZENSHIP,
		Game.REMOVE_CITIZENSHIP,
		Game.IC_UP,
		Game.EFFECT_CONSOLIDATION_UP,
		Game.EFFECT_CONSOLIDATION_DOWN,
		Game.EFFECT_SECURITY_UP,
		Game.EFFECT_SECURITY_DOWN,
		Game.BUY_SHARE,
		Game.VOTE_CONSOLIDATION,
		Game.VOTE_SECURITY,
		Game.VOTE_CONTRAT,
		Game.WIN_BUBBLE,
		Game.LOST_BUBBLE]

	# All the public game_event created with a player should not be transmittable, here is the list
	UNTRANSMITTABLE = [
		Game.EFFECT_CONSOLIDATION_UP,
		Game.EFFECT_CONSOLIDATION_DOWN,
		Game.EFFECT_SECURITY_UP,
		Game.EFFECT_SECURITY_DOWN,
		Game.VOTE_CONSOLIDATION,
		Game.VOTE_SECURITY,
		Game.VOTE_CONTRAT]


class ConcernedPlayers(models.Model):
	player = models.ForeignKey('engine.Player')
	log = models.ForeignKey('logs.Logs')
	# When a run of information tragetting a player is started, we have to gather every Log connected to
	# that players with the attribute transmittable = true
	# And the information of having the information is not transmittable, so we add the player who ordered that run
	# in the many to many fields, but with both personal and transmittable attributes equal to false.
	transmittable = models.BooleanField()
	# personal indicates that the player is the source of the action. Texts must be impacted :
	# 'You have ...' instead of 'Marc have...'
	personal = models.BooleanField()

# Import signals
from logs.signals import *
