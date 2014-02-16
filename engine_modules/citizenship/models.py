# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Player, Order
from engine_modules.corporation.models import Corporation
from messaging.models import Newsfeed


class CitizenShip(models.Model):
	player = models.OneToOneField(Player)
	corporation = models.ForeignKey(Corporation, null=True, on_delete=models.SET_NULL)

	def __unicode__(self):
		return "%s - %s" % (self.player, self.corporation)


class CitizenShipOrder(Order):
	"""
	Order to become citizen from a new corporation
	"""
	title = "Changement de citoyenneté corpo"

	corporation = models.ForeignKey(Corporation)

	def resolve(self):
		self.player.citizenship.corporation = self.corporation
		self.player.citizenship.save()

		# Send a note for final message
		category = u"Citoyenneté"
		content = u"Vous êtes désormais citoyen de la mégacorporation %s." % self.corporation
		newsfeed_content = u"%s est maintenant citoyen de la mégacorporation %s" % (self.player, self.corporation)
		self.player.add_note(category=category, content=content)
		self.player.game.add_newsfeed(category=Newsfeed.PEOPLE, content=newsfeed_content)

	def description(self):
		return u"Récupérer la nationalité corporatiste %s" % self.corporation.base_corporation.name

	def get_form(self, datas=None):
		form = super(CitizenShipOrder, self).get_form(datas)
		form.fields['corporation'].queryset = self.player.game.corporation_set.all()

		return form

orders = (CitizenShipOrder,)
