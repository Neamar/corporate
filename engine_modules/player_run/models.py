# -*- coding: utf-8 -*-
from django.db import models
from django import forms

from engine_modules.run.models import RunOrder
from engine.models import Player
from engine_modules.corporation.models import Corporation
from logs.models import Log, ConcernedPlayer


class InformationOrder(RunOrder):
	"""
	Order for Information runs
	"""
	ORDER = 800
	title = "Lancer une opération d'Information"

	PLAYER_COST = 150
	CORPORATION_COST = 50

	player_targets = models.ManyToManyField(Player, blank=True, help_text='150 k₵ par player')
	corporation_targets = models.ManyToManyField(Corporation, blank=True, help_text='50 k₵ par corporation')

	def __init__(self, *args, **kwargs):
		super(InformationOrder, self).__init__(*args, **kwargs)
		# InformationOrder should not have influence bonus. So we remove it here
		self.has_influence_bonus = False

	def get_form(self, data=None):
		form = super(InformationOrder, self).get_form(data)
		# form.fields['player_targets'].queryset = self.player.game.player_set.all().exclude(pk=self.player.pk)
		# form.fields['corporation_targets'].queryset = self.player.game.corporation_set.all().exclude(pk=self.player.citizenship.corporation.pk if self.player.citizenship.corporation is not None else -1)
		# Remove the additional percents field
		form.fields['player_targets'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=self.player.game.player_set.all().exclude(pk=self.player.pk), required=False, help_text='150 k₵ par player')
		form.fields['corporation_targets'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=self.player.game.corporation_set.all(), required=False, help_text='50 k₵ par corporation')
		# Remove the additional percent field
		form.fields.pop('additional_percents')
		return form

	def description(self):
		players = self.player_targets.all()
		corporations = self.corporation_targets.all()
		player_part = ""
		corporation_part = ""

		if len(players) > 1:
			player_part = "\r\n-les joueurs %s" % (", ".join([p.name for p in players]))
		elif len(players) == 1:
			player_part = "le joueur %s" % players[0].name

		if len(corporations) > 1:
			corporation_part = "\r\n-les corporations %s" % (", ".join([c.base_corporation.name for c in corporations]))
		elif len(corporations) == 1:
			corporation_part = "la corporation %s" % corporations[0].base_corporation.name

		if player_part != "" and corporation_part != "":
			return "Lancer une run d'information sur %s et %s" % (player_part, corporation_part)
		return "Lancer une run d'information sur %s" % (player_part + corporation_part)

	def resolve(self):
		# We override this function to avoid to pay the cost
		self.resolve_successful()

	def pay_cost(self):
		self.player.money -= self.cost
		self.player.save()

	def is_successful(self):
		"""
		Information run always succeed
		"""
		return True

	def resolve_successful(self):
		players = self.player_targets.all()
		corpos = list(self.corporation_targets.all())

		for target in players:
			# Retrieve all event the target could see for himself
			# We need to ask on turn +1 cause we want events related to this turn, right now.
			logs = Log.objects.for_player(target, target, self.player.game.current_turn + 1).exclude(public=True, concernedplayer__transmittable=True)

			for log in logs:
				if not log.concernedplayer_set.filter(player=self.player).exists():
					cp = ConcernedPlayer(
						player=self.player,
						log=log,
						transmittable=False,
						personal=False
					)
					cp.save()

		for target in corpos:
			# Retrieve all event on the corporation
			logs = Log.objects.filter(turn=self.player.game.current_turn, corporation=target).distinct()

			for log in logs:
				if not log.concernedplayer_set.filter(player=self.player).exists():
					cp = ConcernedPlayer(
						player=self.player,
						log=log,
						transmittable=False,
						personal=False
					)
					cp.save()

	def get_cost(self):
		# We cannot calculate the real cost when we save it for the first time. This is beacause We cannot access corporations_taget and player targets
		# before the order is created. So for the first time we give the minimum and then we use the get_cost() function and not the oreder.cost value
		dumb_result = 0
		return self.get_real_cost() if self.pk is not None else dumb_result

	def get_real_cost(self):
		return self.player_targets.count() * self.PLAYER_COST + self.corporation_targets.count() * self.CORPORATION_COST

	def custom_description(self):
		return ""

orders = (InformationOrder, )
