# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Order
from engine_modules.corporation.models import Corporation
from engine_modules.derivative.models import Derivative
from messaging.models import Note


class AbstractSpeculation(Order):
	"""
	Base class for speculation.
	"""
	class Meta:
		abstract = True

	MAX_AMOUNT_SPECULATION = 100
	BASE_COST = 1

	investment = models.PositiveIntegerField(help_text="En milliers de nuyens.")
	on_win_ratio = models.PositiveSmallIntegerField(default=1, editable=False)
	on_loss_ratio = models.PositiveSmallIntegerField(default=1, editable=False)

	def get_cost(self):
		return (self.investment or 0) * self.BASE_COST

	def on_win_money(self):
		"""
		Money gained when speculation worked
		"""
		return self.get_cost() * self.on_win_ratio

	def on_loss_money(self):
		"""
		Money losed when speculation failed
		"""
		return self.get_cost() * self.on_loss_ratio


class CorporationSpeculationOrder(AbstractSpeculation):
	"""
	Order to speculate on a corporation's rank
	"""
	ORDER = 900
	title = "Spéculer sur une corporation"

	corporation = models.ForeignKey(Corporation)
	rank = models.PositiveSmallIntegerField()

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('on_win_ratio', 4)
		super(CorporationSpeculationOrder, self).__init__(*args, **kwargs)

	def resolve(self):
		ladder = self.player.game.get_ladder()

		# Build message

		if ladder.index(self.corporation) + 1 == self.rank:
			self.player.money += self.on_win_money()
			self.player.save()
			content = u"Vos investissements de %sk ¥ sur la corporation %s vous ont rapporté %sk ¥" % (self.investment, self.corporation.base_corporation.name, self.on_win_money())
		else:
			# Failure
			self.player.money -= self.on_loss_money()
			self.player.save()
			content = u"Vos spéculations de %sk ¥ sur la corporation %s n'ont malheureusement pas été concluantes" % (self.investment, self.corporation.base_corporation.name)

		self.player.add_note(category=Note.SPECULATION, content=content)

	def description(self):
		return u"Miser sur la position %s de la corporation %s (gain : %sk¥, perte : %sk¥)" % (self.rank, self.corporation.base_corporation.name, (self.on_win_money() + self.get_cost()), self.on_loss_money())


class DerivativeSpeculationOrder(AbstractSpeculation):
	"""
	Order to speculate on a derivative up or down
	"""
	ORDER = 1000
	UP = True
	DOWN = False

	UPDOWN_CHOICES = (
		(UP, 'à la hausse'),
		(DOWN, 'à la baisse')
	)

	title = "Spéculer sur un produit dérivé"

	speculation = models.BooleanField(choices=UPDOWN_CHOICES)
	derivative = models.ForeignKey(Derivative)

	def resolve(self):
		# Build message
		current_turn_sum = self.derivative.get_sum(self.player.game.current_turn)
		previous_turn_sum = self.derivative.get_sum(self.player.game.current_turn - 1)
		if (current_turn_sum > previous_turn_sum and self.speculation == self.UP) or (current_turn_sum < previous_turn_sum and self.speculation == self.DOWN):
			# Success
			self.player.money += self.on_win_money()
			self.player.save()
			content = u"Vos spéculations de %sk ¥ sur le produit dérivé %s vous ont rapporté %sk ¥" % (self.investment, self.derivative.name, self.on_win_money())
		else:
			# Failure
			self.player.money -= self.on_loss_money()
			self.player.save()
			content = u"Vos spéculations de %sk ¥ sur le produit dérivé %s n'ont malheureusement pas été concluantes" % (self.investment, self.derivative.name)

		self.player.add_note(category=Note.SPECULATION, content=content)

	def description(self):
		return u"Miser %s du produit dérivé %s (gain : %sk¥, perte : %sk¥)" % (self.get_speculation_display(), self.derivative.name, (self.on_win_money() + self.get_cost()), self.on_loss_money())

orders = (CorporationSpeculationOrder, DerivativeSpeculationOrder)
