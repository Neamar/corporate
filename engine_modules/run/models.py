# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from random import randint

from engine.models import Order
from engine_modules.detroit_inc.models import DIncVoteOrder


class RunOrder(Order):
	"""
	Base model for all runs
	"""
	MAX_PERCENTS = 90
	MAX_SELECTABLE = 90

	LAUNCH_COST = 350
	BASE_COST = 50
	BASE_SUCCESS_PROBABILITY = 50
	INFLUENCE_BONUS = 500

	has_RSEC_bonus = models.BooleanField(default=False, editable=False)
	additional_percents = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(20), MinValueValidator(0)])
	hidden_percents = models.SmallIntegerField(default=0, editable=False)

	def __init__(self, *args, **kwargs):
		super(RunOrder, self).__init__(*args, **kwargs)

	def save(self):
		super(RunOrder, self).save()

	def get_raw_probability(self):
		"""
		Compute intended success probability, no max
		Should only be used to compute the resolve order of runs
		"""
		proba = RunOrder.BASE_SUCCESS_PROBABILITY
		proba += (self.additional_percents + self.hidden_percents) * 10
		return proba

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		return min(self.get_raw_probability(), RunOrder.MAX_PERCENTS)

	def is_successful(self):
		"""
		Return true if the run is successful (random call, non omnipotent)
		"""
		return randint(1, 100) <= self.get_success_probability()

	def resolve(self):
		"""
		Check whether the run is successful or not,
		Make the player pay for his order,
		Resolve actions
		"""
		self.player.money -= self.get_cost()
		self.player.save()

		result = self.is_successful()
		if result:
			self.resolve_successful()
		else:
			self.resolve_failure()
		return result

	def resolve_to_fail(self):
		"""
		Used to force a run to fail
		"""
		self.player.money -= self.get_cost()
		self.player.save()

		self.resolve_failure()
		return False

	def resolve_successful(self):
		"""
		This function is called when the run has succeeded

		It must be overriden.
		"""
		raise NotImplementedError()

	def resolve_failure(self):
		"""
		This function is called when the run has failed.

		It can be overriden and does nothing by default.
		"""
		pass

	def calc_cost(self, additional_percents):
		# base cost = 0 for the first run if you vote RSEC and this coalition succeeded and current turn is not the last
		if self.player.game.current_turn < self.player.game.total_turn:
			if self.player.game.get_dinc_coalition() == DIncVoteOrder.RSEC:
				if self.player.get_last_dinc_coalition() == DIncVoteOrder.RSEC:
					# We have to check for other RunOrders with has_RSEC_bonus set to True,
					# so we can know if it is possible to have another one with an influence bonus
					# I have not investigated much, but it looks like this has a big impact
					# performance-wise
					# OK, this is less than ideal, but the other way REALLY had poor performance
					RunOrderTypes = ['SabotageOrder', 'ExtractionOrder', 'DataStealOrder', 'ProtectionOrder']
					orders = self.player.order_set.filter(type__in=RunOrderTypes, runorder__has_RSEC_bonus=True, turn=self.player.game.current_turn)

					if len(orders) < 1:
						self.has_RSEC_bonus = True
						# We have an infite loop in the save function in case a cost is not defined
						if self.cost:
							self.save()
		cost = RunOrder.LAUNCH_COST
		cost += RunOrder.BASE_COST * additional_percents

		# Do not pay for the influence bonus
		if self.has_RSEC_bonus:
			cost -= RunOrder.INFLUENCE_BONUS
		return max(cost, 0)

	def get_cost(self):
		return self.calc_cost(self.additional_percents)

	def get_form(self, data=None):
		form = super(RunOrder, self).get_form(data)
		# We remove has_RSEC_bonus because we want to handle it automatically
		max_additional_percents = self.MAX_SELECTABLE - self.BASE_SUCCESS_PROBABILITY
		values = range(0, ((max_additional_percents) / 10) + 1)
		form.fields['additional_percents'].widget = forms.Select(choices=((i, u"{1} k₵ - précision {0}".format(self.BASE_SUCCESS_PROBABILITY + i * 10, self.calc_cost(i))) for i in values))
		form.fields['additional_percents'].label = u'Prix'
		return form

	def custom_description(self):
		return "%s%%" % self.get_raw_probability()
