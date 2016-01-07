# -*- coding: utf-8 -*-
from django.db import models
from engine.models import Order, Game
from engine_modules.corporation.models import Corporation


class AbstractSpeculation(Order):
	"""
	Base class for speculation.
	"""
	class Meta:
		abstract = True

	MAX_AMOUNT_SPECULATION = 200
	BASE_COST = 1

	investment = models.PositiveIntegerField(help_text="En k₵")
	on_win_ratio = models.PositiveSmallIntegerField(default=1, editable=False)
	on_loss_ratio = models.PositiveSmallIntegerField(default=1, editable=False)

	def get_cost(self):
		# or 1: avoid displaying the order when the player has no money left
		return (self.investment or 1) * self.BASE_COST

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

		if ladder.index(self.corporation) + 1 == self.rank:
			# Well done!
			self.player.money += self.on_win_money()
			self.player.save()
			self.player.game.add_event(event_type=Game.SPECULATION_WIN, data={"player": self.player.name, "mise": self.investment, "corporation": self.corporation.base_corporation.name, "position": self.rank, "total_win": self.on_win_money()}, players=[self.player])
		else:
			# Failure
			self.player.money -= self.on_loss_money()
			self.player.save()
			self.player.game.add_event(event_type=Game.SPECULATION_LOST, data={"player": self.player.name, "mise": self.investment, "corporation": self.corporation.base_corporation.name, "position": self.rank}, players=[self.player])

	def description(self):
		return u"Miser sur la position %s de la corporation %s (gain : %sk₵, perte : %sk₵)" % (self.rank, self.corporation.base_corporation.name, (self.on_win_money() + self.get_cost()), self.on_loss_money())


orders = (CorporationSpeculationOrder, )
