# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Player, Order
from engine_modules.corporation.models import Corporation

class CitizenShip(models.Model):
	player = models.OneToOneField(Player)
	corporation = models.ForeignKey(Corporation, null=True)


class CitizenShipOrder(Order):
	"""
	Order to become citizen from a new corporation
	"""
	corporation = models.ForeignKey(Corporation)

	def resolve(self):
		self.player.citizenship.corporation = self.corporation
		self.player.citizenship.save()
		
		# Send a note for final message
		category=u"Citoyenneté"
		content=u"Vous êtes désormais citoyen de la mégacorporation %s." % self.corporation
		global_content=u"%s est maintenant citoyen de la mégacorporation %s" % (self.player, self.corporation)
		self.player.add_note(category=category, content=content)
		self.player.game.add_note(category=category, content=global_content)

	def description(self):
		return u"Récupérer la nationalité corporatiste %s" % self.corporation.base_corporation.name

orders = (CitizenShipOrder,)
