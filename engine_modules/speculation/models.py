# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum
from engine.models import Order, Game
from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory


class Derivative(models.Model):
	name = models.CharField(max_length=30)
	game = models.ForeignKey(Game)
	corporations = models.ManyToManyField(Corporation)

	def __unicode__(self):
		return self.name


class CorporationSpeculationOrder(Order):
	"""
	Order to speculate on a corporation's rank
	"""
	MAX_AMOUNT_SPECULATION = 50
	BASE_COST = 1

	title = "Spéculer sur une corporation"

	corporation = models.ForeignKey(Corporation)
	rank = models.PositiveSmallIntegerField()
	investment = models.PositiveIntegerField(help_text="En milliers de nuyens.")
	on_win_ratio = models.PositiveSmallIntegerField(default=4, editable=False)
	on_loss_ratio = models.PositiveSmallIntegerField(default=1, editable=False)

	def get_cost(self):
		return self.investment * self.BASE_COST

	def resolve(self):
		ladder = self.player.game.get_ordered_corporations()

		# Build message
		category = u"Spéculations"

		if ladder.index(self.corporation) + 1 == self.rank:
			self.player.money += self.get_cost() * self.on_win_ratio
			self.player.save()
			content = u"Vos investissements de %sk ¥ sur la corporation %s vous ont rapporté %sk ¥" % (self.investment, self.corporation.base_corporation.name, self.investment * self.on_win_ratio)
		else:
			# Failure
			self.player.money -= self.get_cost() * self.on_loss_ratio
			self.player.save()
			content = u"Vos spéculations de %sk ¥ sur la corporation %s n'ont malheureusement pas été concluantes" % (self.investment, self.corporation.base_corporation.name)

		self.player.add_note(category=category, content=content)

	def description(self):
		return u"Miser %sk ¥ sur la position %s de la corporation %s (1 pour %s)" % (self.get_cost(), self.rank, self.corporation.base_corporation.name, self.on_win_ratio)


class DerivativeSpeculationOrder(Order):
	"""
	Order to speculate on a derivative up or down
	"""
	MAX_AMOUNT_SPECULATION = 50
	BASE_COST = 1

	UP = True
	DOWN = False

	UPDOWN_CHOICES = (
		(UP, 'à la hausse'),
		(DOWN, 'à la baisse')
	)

	title = "Spéculer sur un produit dérivé"

	speculation = models.BooleanField(choices=UPDOWN_CHOICES)
	derivative = models.ForeignKey(Derivative)
	investment = models.PositiveIntegerField(help_text="En milliers de nuyens.")
	on_win_ratio = models.PositiveSmallIntegerField(default=1)
	on_loss_ratio = models.PositiveSmallIntegerField(default=1)

	def get_cost(self):
		return self.investment * self.BASE_COST

	def resolve(self):
		# Build message
		category = u"Spéculations"
		current_turn_sum = AssetHistory.objects.filter(corporation__in=self.derivative.corporations.all(), turn=self.player.game.current_turn).aggregate(Sum('assets'))['assets__sum']
		previous_turn_sum = AssetHistory.objects.filter(corporation__in=self.derivative.corporations.all(), turn=self.player.game.current_turn - 1).aggregate(Sum('assets'))['assets__sum']
		if current_turn_sum > previous_turn_sum and self.speculation == self.UP:
			# Success
			self.player.money += self.get_cost() * self.on_win_ratio
			self.player.save()
			content = u"Vous êtes un bon spéculateur, vos investissements de %sk ¥ sur le produit dérivé %s vous ont rapporté %sk ¥" % (self.investment, self.derivative.name, self.investment * self.on_win_ratio)
		else:
			# Failure
			self.player.money -= self.get_cost() * self.on_loss_ratio
			self.player.save()
			content = u"Vos spéculations de %sk ¥ sur le produit dérivé %s n'ont malheureusement pas été concluantes" % (self.investment, self.derivative.name)

		self.player.add_note(category=category, content=content)

	def description(self):
		return u"Miser %sk ¥ %s du produit dérivé %s (1 pour %s)" % (self.get_cost(), self.get_speculation_display(), self.derivative.name, self.on_win_ratio)


orders = (CorporationSpeculationOrder, DerivativeSpeculationOrder)
