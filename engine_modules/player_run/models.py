# -*- coding: utf-8 -*-
from django.db import models, IntegrityError

from engine_modules.run.models import RunOrder
from engine.models import Player
from logs.models import Log, ConcernedPlayer


information_messages = {
	'success': {
		'sponsor': u"Votre équipe a *réussi* une run d'**Information** sur %s",
		'citizens': u"Une run d'**Information**, commanditée par %s, a *réussi* sur %s avec %s%% chances de réussite",
	},
	'fail': {
		'sponsor': u"Votre équipe a *échoué* sa run d'**Information** sur %s",
		'citizens': u"Une run d'**Information**, commanditée par %s, a *échoué* sur %s avec %s%% chances de réussite",
	},
}


class InformationOrder(RunOrder):
	"""
	Order for Information runs
	"""
	ORDER = 800
	title = "Lancer une run d'Information"

	PROTECTION_TYPE = "datasteal"

	target = models.ForeignKey(Player)

	# TODO def resolve_successful(self):

	# TODO def resolve_failure(self):

	def get_form(self, data=None):
		form = super(InformationOrder, self).get_form(data)

		form.fields['target'].queryset = self.player.game.player_set.all().exclude(pk=self.player.pk)
		return form

	def description(self):
		return "Lancer une run d'information sur %s (%s%%)" % (self.target, self.get_raw_probability())

	def resolve_successful(self):
		# Retrieve all event the target could see for himself
		# We need to ask on turn +1 cause we cant events related to this turn, right now.
		logs = Log.objects.for_player(self.target, self.target, self.player.game.current_turn + 1).exclude(public=True)

		for log in logs:
			if not log.concernedplayer_set.filter(player=self.player).exists():
				cp = ConcernedPlayer(
					player=self.player,
					log=log,
					transmittable=False,
					personal=False
				)
				cp.save()

orders = (InformationOrder, )
