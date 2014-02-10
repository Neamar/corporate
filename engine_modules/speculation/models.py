# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum
from engine.models import Order
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory


class Derivative(models.Model):
	name = models.CharField(max_length=30)
	corporations = models.ManyToManyField(Corporation)


class CorporationSpeculationOrder(Order):
	"""
	Order to speculate on a corporation's rank
	"""
	MAX_AMOUNT_SPECULATION = 50
	BASE_COST = 1

	title = "Spéculer sur une corporation"

	corporation = models.ForeignKey(Corporation)
	rank = models.PositiveSmallIntegerField()
	investment = models.PositiveIntegerField()

	def get_cost(self):
		return self.investment * self.BASE_COST

	def resolve(self):
		ladder = self.player.game.get_ordered_corporations()

		# Build message
		category = u"Spéculations"

		if ladder.index(self.corporation) + 1 == self.rank:
			# Success
			if self.corporation == ladder[0] or self.corporation == ladder[-1]:
				# Speculation on first or last corpo
				self.player.money += self.get_cost() * 2
				self.player.save()
				content = u"Vous êtes un bon spéculateur, vos investissements sur la corporation %s vous ont rapporté %s" % (self.corporation.base_corporation.name, self.investment * 3)
			else:
				# Speculation on non first or non last corpo
				self.player.money += self.get_cost() * 4
				self.player.save()
				content = u"Vous êtes un excellent spéculateur, vos investissements sur la corporation %s vous ont rapporté %s" % (self.corporation.base_corporation.name, self.investment * 5)
		else:
			# Failure
			self.player.money -= self.get_cost()
			self.player.save()
			content = u"Vos spéculations sur la corporation %s n'ont malheureusement pas été concluantes" % self.corporation.base_corporation.name

		self.player.add_note(category=category, content=content)

	def description(self):
		return u"Miser %s ¥ sur la postion %s de la corporation %s" % (self.get_cost(), self.rank, self.corporation.base_corporation.name)


class DerivativeSpeculationOrder(Order):
	"""
	Order to speculate on a derivative up or down
	"""
	MAX_AMOUNT_SPECULATION = 50
	BASE_COST = 10

	UP = True
	DOWN = False

	UPDOWN_CHOICES = (
		(UP, 'up'),
		(DOWN, 'down')
	)

	title = "Spéculer sur un produit dérivé"

	speculation = models.BooleanField(choices=UPDOWN_CHOICES)
	derivative = models.ForeignKey(Derivative)
	investment = models.PositiveIntegerField()

	def get_cost(self):
		return self.investment * self.BASE_COST

	def resolve(self):

		# Build message
		category = u"Spéculations"
		current_turn_sum = AssetHistory.objects.filter(corporation__in=self.derivative.corporations.all(), turn=self.player.game.current_turn).aggregate(Sum('assets'))['assets__sum']
		previous_turn_sum = AssetHistory.objects.filter(corporation__in=self.derivative.corporations.all(), turn=self.player.game.current_turn - 1).aggregate(Sum('assets'))['assets__sum']
		if current_turn_sum > previous_turn_sum and self.speculation == self.UP:
			# Success
			self.player.money += self.get_cost() * 2
			self.player.save()
			content = u"Vous êtes un bon spéculateur, vos investissements sur le produit dérivé %s vous ont rapporté %s" % (self.derivative.name, self.investment * 2)
		else:
			# Failure
			self.player.money -= self.get_cost()
			self.player.save()
			content = u"Vos spéculations sur le produit dérivé %s n'ont malheureusement pas été concluantes" % self.derivative.name

		self.player.add_note(category=category, content=content)

	def description(self):
		if self.speculation == self.UP:
			return u"Miser %s ¥ à la hausse du produit dérivé %s" % (self.get_cost(), self.derivative.name)
		else:
			return u"Miser %s ¥ à la baisse du produit dérivé %s" % (self.get_cost(), self.derivative.name)


orders = (CorporationSpeculationOrder, DerivativeSpeculationOrder)
