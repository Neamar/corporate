# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Game


class Logs(models.Model):

	turn = models.PositiveSmallIntegerField()
	game = models.ForeignKey('engine.Game')
	delta = models.SmallIntegerField()
	# some icons must be duplicated for display on corporation but not on the players
	# for example we want a +1 and a -1 icon for an extraction but just one extraction icon on the plyer who order it
	# So the -1 Log is hidden for players to just have one icon
	hide_for_players = models.BooleanField()
	# To avoid attaching public info on all 8 players and simplify end_game request we created a flag 'public'
	public = models.BooleanField()
	# All the categories are defined just before, 1 category = 1 icon
	event_type = models.CharField(max_length=30, choices=Game.EVENTS)
	# data contains a json with all the informations needed for the text.
	data = models.TextField()
	corporation = models.ForeignKey('corporation.Corporation', null=True)
	corporationmarket = models.ForeignKey('market.CorporationMarket', null=True)
	players = models.ManyToManyField('engine.Player', null=True)

	HIDE_FOR_PLAYERS = [
		Game.OPE_DATASTEAL_FAIL_DOWN,
		Game.OPE_DATASTEAL_DOWN,
		Game.OPE_EXTRACTION_FAIL_DOWN,
		Game.OPE_EXTRACTION_DOWN]

	PUBLIC = [
		Game.FIRST_EFFECT,
		Game.LAST_EFFECT,
		Game.CRASH_EFFECT,
		Game.EFFECT_DEV_URBAIN_UP,
		Game.EFFECT_DEV_URBAIN_DOWN,
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
		Game.VOTE_DEV_URBAIN]

	UNTRANSMITTABLE = [
		Game.EFFECT_CONSOLIDATION_UP,
		Game.EFFECT_CONSOLIDATION_DOWN,
		Game.EFFECT_SECURITY_UP,
		Game.EFFECT_SECURITY_DOWN]


class ConcernedPlayers(models.Model):
	player = models.ForeignKey('engine.Player')
	log = models.ForeignKey('logs.Logs')
	# A transmittable log for a player is given to a
	# When a run of information that targets a player is started, we have to gather every Log connected to
	# that players with the attribute transmittable = true
	# And the information of having the information is not transmittable, so we add the player who ordered that run
	# in the many to many fields, but with both personal and transmittable attributes equal to false.
	transmittable = models.BooleanField()
	# It indicates that the player is the source of the action. Texts must be impacted :
	# 'You have ...' instead of 'Marc have...'
	personal = models.BooleanField()
