# -*- coding: utf-8 -*-
import json
from django.db import models
from engine.models import Game


class Log(models.Model):
	"""
	We log every action in the game in a single table
	"""
	turn = models.PositiveSmallIntegerField()
	game = models.ForeignKey('engine.Game')

	# how much assets are lost or won on a market
	delta = models.SmallIntegerField()

	# some icons must be duplicated for display on a corporation but not on a player
	# for example we want a +1 and a -1 icon for an extraction but just one extraction icon on the player who orders it
	# So the -1 Log is hidden for players to just have one icon
	hide_for_players = models.BooleanField()

	# To avoid attaching public info on all 8 players and simplify end_game request we created a flag 'public'
	public = models.BooleanField()

	# An event_type is a type of game_event. All game_events are defined in Game
	event_type = models.CharField(max_length=30)

	# data contains a json with all the informations needed for the text.
	data = models.TextField()

	# the corporation concerned by the log
	corporation = models.ForeignKey('corporation.Corporation', null=True)

	# the corporationmarket concerned for this log
	corporation_market = models.ForeignKey('market.CorporationMarket', null=True)

	# the orderer of the action and all the players knowing the action. Parameters are different between orderer and knowers, see ConcernedPlayer
	players = models.ManyToManyField('engine.Player', through='ConcernedPlayer')

	# List of game events that are hidden for players (see hide for player above)
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
		Game.GAIN_DOMINATION_BUBBLE,
		Game.LOSE_DOMINATION_BUBBLE,
		Game.GAIN_DRY_BUBBLE,
		Game.LOSE_DRY_BUBBLE]

	# All the public game_event created with a player should not be transmittable, here is the list
	UNTRANSMITTABLE = [
		Game.EFFECT_CONSOLIDATION_UP,
		Game.EFFECT_CONSOLIDATION_DOWN,
		Game.EFFECT_SECURITY_UP,
		Game.EFFECT_SECURITY_DOWN,
		Game.VOTE_CONSOLIDATION,
		Game.VOTE_SECURITY,
		Game.VOTE_CONTRAT]

	def get_display(self, type, display_context, isPersonal=False):
		if isPersonal:
			pathPersonal = 'personal'
		else:
			pathPersonal = 'not_personal'
		file_name = self.event_type
		messages_context = json.loads(self.data)
		path = 'logs/%s/%s/%s.md' % (pathPersonal, display_context, file_name.lower())
		template = get_template(path)
		text, other = template.render(messages_context)
		return "GET DISPLAY %s: %s" % (type, text)


class ConcernedPlayer(models.Model):
	player = models.ForeignKey('engine.Player')
	log = models.ForeignKey('logs.Log')
	# When an information run targetting a player is started, we have to gather every Log connected to
	# that player with the attribute transmittable = True
	# And the information of having the information is not transmittable, so we add the player who ordered that run
	# in the many to many fields, but with both personal and transmittable attributes equal to false.
	transmittable = models.BooleanField()
	# personal indicates that the player is the source of the action. Texts must be impacted :
	# 'You have ...' instead of 'Marc have...'
	personal = models.BooleanField()

# Import signals
from logs.signals import *
