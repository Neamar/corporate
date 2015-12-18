# -*- coding: utf-8 -*-
from django.db import models

from engine_modules.run.models import RunOrder
from engine.models import Player, Game
from engine_modules.corporation.models import Corporation
from logs.models import Log, ConcernedPlayer


class InformationOrder(RunOrder):
	"""
	Order for Information runs
	"""
	ORDER = 800
	title = "Lancer une run d'Information"

	PLAYER_COST = 150
	CORPORATION_COST = 50

	player_targets = models.ManyToManyField(Player)
	corporation_targets = models.ManyToManyField(Corporation)

	def get_form(self, data=None):
		form = super(InformationOrder, self).get_form(data)

		form.fields['player_targets'].queryset = self.player.game.player_set.all().exclude(pk=self.player.pk)
		form.fields['corporation_targets'].queryset = self.player.game.corporation_set.all().exclude(pk=self.player.citizenship.corporation if self.player.citizenship is not None else -1)

		return form

	def description(self):
		return "Lancer une run d'information sur %s (%s%%)" % (self.target, self.get_raw_probability())

	def is_successful(self):
		"""
		Information run always succeed
		"""
		return True

	def resolve_successful(self):
		players = self.player_targets.all()
		corpos = list(self.corporation_targets.all())

		if self.player.citizenship is not None:
			corpos.append(self.player.citizenship.corporation)

		self.player.game.add_event(event_type=Game.OPE_INFORMATION, data={"players_list": [p.name for p in players], "corpos_list": [c.base_corporation.name for c in corpos]}, players=[self.player])

		for target in players:
			# Retrieve all event the target could see for himself
			# We need to ask on turn +1 cause we want events related to this turn, right now.
			logs = Log.objects.for_player(target, target, self.player.game.current_turn + 1).exclude(public=True)

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
		return self.player_targets.count() * self.PLAYER_COST + self.corporation_targets.count() * self.CORPORATION_COST if self.pk is not None else self.CORPORATION_COST

orders = (InformationOrder, )
