# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from engine.models import Player, Order, Game
from engine_modules.corporation.models import Corporation


class Share(models.Model):
	"""
	A share held by some player
	"""
	corporation = models.ForeignKey(Corporation)
	player = models.ForeignKey(Player)
	turn = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return u"%s share for %s" % (self.corporation, self.player)


class BuyShareOrder(Order):
	"""
	Order to buy a corporation share
	"""
	title = "Acheter une part dans une corporation"
	ORDER = 100
	BASE_COST = 100
	FIRST_COST = 125
	FIRST_AND_CITIZEN_COST = 100

	corporation = models.ForeignKey(Corporation)

	def get_cost(self):
		if not hasattr(self, "corporation"):
			# avoid displaying the order when the player can't affort the cheapest
			return self.player.game.get_ladder()[-1].assets * BuyShareOrder.BASE_COST
		elif self.corporation == self.player.game.get_ladder()[0]:
			if self.player.citizenship.corporation != self.corporation:
				return BuyShareOrder.FIRST_COST * self.corporation.assets
			else:
				return BuyShareOrder.FIRST_AND_CITIZEN_COST * self.corporation.assets
		else:
			return BuyShareOrder.BASE_COST * self.corporation.assets

	def get_priced_list(self):
		dropdownchoices = self.player.game.get_ladder()
		first = True
		for corporation in dropdownchoices:
			if first:
				if self.player.citizenship.corporation != corporation:
					corporation.text = u"{0} ({1} actifs) - {2} k₵".format(corporation.base_corporation.name, corporation.assets, BuyShareOrder.FIRST_COST * corporation.assets)
				else:
					corporation.text = u"{0} ({1} actifs) - {2} k₵".format(corporation.base_corporation.name, corporation.assets, BuyShareOrder.FIRST_AND_CITIZEN_COST * corporation.assets)
			else:
				corporation.text = u"{0} ({1} actifs) - {2} k₵".format(corporation.base_corporation.name, corporation.assets, BuyShareOrder.BASE_COST * corporation.assets)
			first = False
		return dropdownchoices

	def resolve(self):
		# Pay.
		price = self.get_cost()
		self.player.money -= price
		self.player.save()

		# Add a share to the player
		Share(
			corporation=self.corporation,
			player=self.player
		).save()

		# Create game_event
		self.player.game.add_event(event_type=Game.BUY_SHARE, data={"player": self.player.name, "corporation": self.corporation.base_corporation.name, 'cost': price}, corporation=self.corporation, players=[self.player])

	def description(self):
		return u"Acheter une part de la corporation %s (actifs actuels : %s)" % (self.corporation.base_corporation.name, self.corporation.assets)

	def get_form(self, data=None):
		form = super(BuyShareOrder, self).get_form(data)
		#form.fields['corporation'].widget = forms.Select(choices=((corporation.id, corporation.text) for corporation in self.get_priced_list()))
		form.fields['corporation'].widget = forms.Select(choices=[('', '---------')] + [(corporation.id, corporation.text) for corporation in self.get_priced_list()])
		form.initial['corporation'] = ''

		return form

orders = (BuyShareOrder,)
