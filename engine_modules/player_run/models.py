# -*- coding: utf-8 -*-
from django.db import models

from engine_modules.run.models import RunOrder
from engine.models import Player
from website.widgets import PlainTextField


class InformationOrder(RunOrder):
	"""
	Order for Information runs
	"""
	ORDER = 800
	title = "Lancer une run d'Information"

	PROTECTION_TYPE = "datasteal"
	BASE_SUCCESS_PROBABILITY = 60

	target = models.ForeignKey(Player)

	# TODO def resolve_successful(self):

	# TODO def resolve_failure(self):

	def get_form(self, data=None):
		form = super(InformationOrder, self).get_form(data)
		form.fields['base_percents'] = PlainTextField(initial="%s%%" % self.BASE_SUCCESS_PROBABILITY)

		form.fields['target'].queryset = self.player.game.player_set.all().exclude(pk=self.player.pk)
		return form

	def description(self):
		return "Lancer une run d'information sur %s (%s%%)" % (self.target, self.get_raw_probability())

orders = (InformationOrder, )
