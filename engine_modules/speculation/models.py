# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Order
from engine_modules.corporation.models import Corporation


class SpeculationOrder(Order):
	"""
	Order to speculate on a corporation's rank
	"""

	BASE_COST = 10

	corporation = models.ForeignKey(Corporation)
	rank = models.PositiveSmallIntegerField()
	investment = models.PositiveIntegerField()


	def get_cost(self):
		return self.investment * self.BASE_COST


	def resolve(self):
		ladder = self.player.game.get_ordered_corporations()
		corpo = self.corporation

		# Build message
		category = u"Spéculations"

		# Success
		if ladder.index(corpo) + 1 == self.rank:
			# Speculation on first or last corpo
			if corpo == ladder[0] or corpo == ladder[-1]:
				self.player.money += self.get_cost() * 2
				self.player.save()
				content = u"Vous êtes un bon spéculateur, vos investissements vous ont rapporté %s" % self.investment * 3
			# Speculation on non first or non last corpo
			else:
				self.player.money += self.get_cost() * 4
				self.player.save()
				content = u"Vous êtes un excellent spéculateur, vos investissements vous ont rapporté %s" % self.investment * 5
		# Failure
		else:
			self.player.money -= self.get_cost()
			self.player.save()
			content = u"Vos spéculations n'ont malheureusement pas étés concluantes"

		self.player.add_note(category=category, content=content)

	def description(self):
		return u"Spéculer sur le classement d'un corporation"


orders = (SpeculationOrder,)