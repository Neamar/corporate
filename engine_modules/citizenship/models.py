# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Player, Order, Game
from engine_modules.corporation.models import Corporation


class Citizenship(models.Model):
	player = models.ForeignKey(Player)
	corporation = models.ForeignKey(Corporation, null=True, on_delete=models.SET_NULL, label="test")
	turn = models.PositiveSmallIntegerField(default=0)

	def __unicode__(self):
		return u"%s - %s" % (self.player, self.corporation)


class CitizenshipOrder(Order):
	"""
	Order to become citizen from a new corporation
	"""
	ORDER = 400
	title = "Changer de citoyenneté corpo"

	corporation = models.ForeignKey(Corporation)

	def resolve(self):
		# if player has a citizenship, add a game_event for losing it
		corporation_last_turn = self.player.citizenship.corporation
		if corporation_last_turn is not None:
			self.player.game.add_event(event_type=Game.REMOVE_CITIZENSHIP, data={"player": self.player.name, "corporation": corporation_last_turn.base_corporation.name}, corporation=corporation_last_turn, players=[self.player])

		citizenship = self.player.citizenship_set.get(turn=self.turn)
		citizenship.corporation = self.corporation
		citizenship.save()

		# create a game_event for the new citizenship
		self.player.game.add_event(event_type=Game.ADD_CITIZENSHIP, data={"player": self.player.name, "corporation": self.corporation.base_corporation.name}, corporation=self.corporation, players=[self.player])

	def description(self):
		return u"Récupérer la nationalité corporatiste %s" % self.corporation.base_corporation.name

	def get_form(self, data=None):
		form = super(CitizenshipOrder, self).get_form(data)
		inner_qs = self.player.share_set.all().values("corporation")
		form.fields['corporation'].queryset = self.player.game.corporation_set.filter(pk__in=inner_qs)
		return form

orders = (CitizenshipOrder,)
