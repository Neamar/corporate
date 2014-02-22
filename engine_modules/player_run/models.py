# -*- coding: utf-8 -*-
from django.db import models
from engine_modules.run.models import RunOrder
from engine.models import Player
from messaging.models import Message


class InformationRunOrder(RunOrder):
	title = "Lancer une run d'Information"

	target = models.ForeignKey(Player)

	def resolve_successful(self):
		target_orders = self.target.message_set.filter(flag=Message.RESOLUTION).order_by('-turn')

		self.player.add_message(
			title="Run d'information sur %s" % (self.target),
			content="\n".join(["## Tour %s\n\n%s" % (o.turn, o.content) for o in target_orders]),
			author=None,
			flag=Message.PRIVATE_MESSAGE,
		)

	def description(self):
		return "Lancer une run d'information sur %s" % self.target

orders = (InformationRunOrder, )
