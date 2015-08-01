# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Player, Order
from engine_modules.corporation.models import Corporation


class CitizenShip(models.Model):
	player = models.OneToOneField(Player)
	corporation = models.ForeignKey(Corporation, null=True, on_delete=models.SET_NULL)

	def __unicode__(self):
		return "%s - %s" % (self.player, self.corporation)


class CitizenShipOrder(Order):
	"""
	Order to become citizen from a new corporation
	"""
	ORDER = 400
	title = "Changer de citoyenneté corpo"

	corporation = models.ForeignKey(Corporation)

	def resolve(self):
		self.player.citizenship.corporation = self.corporation
		self.player.citizenship.save()

	def description(self):
		return u"Récupérer la nationalité corporatiste %s" % self.corporation.base_corporation.name

	def get_form(self, data=None):
		form = super(CitizenShipOrder, self).get_form(data)
		form.fields['corporation'].queryset = self.player.game.corporation_set.all()
		return form

orders = (CitizenShipOrder,)
