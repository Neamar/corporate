# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Order
from engine_modules.corporation.models import Corporation

class VoteOrder(Order):
	"""
	Order to vote for a Corporation
	"""
	corporation_up = models.ForeignKey(Corporation, related_name="+")
	corporation_down = models.ForeignKey(Corporation, related_name="+")

	def resolve(self):
		self.corporation_up.assets += 1
		self.corporation_up.save()

		self.corporation_down.assets -= 1
		self.corporation_down.save()

	def description(self):
		return u"Voter pour l'augmentation des actifs de %s et la diminution de %s" % (self.corporation_up.base_corporation.name, self.corporation_down.base_corporation.name)

orders = (VoteOrder,)

