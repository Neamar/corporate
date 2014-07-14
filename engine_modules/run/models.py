# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from random import randint

from engine.models import Order


class RunOrder(Order):
	"""
	Base model for all runs
	"""
	MAX_PERCENTS = 90

	LAUNCH_COST = 350
	BASE_COST = 50
	BASE_SUCCESS_PROBABILITY = 50
	INFLUENCE_BONUS = 300

	has_influence_bonus = models.BooleanField(default=False, help_text="Accorder à cette run une remise de 300k")
	additional_percents = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(20), MinValueValidator(1)], help_text="Palier de 10% supplémentaires.")
	hidden_percents = models.SmallIntegerField(default=0, editable=False)

	def clean(self):
		super(RunOrder, self).clean()

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
		Return true if the run is successful (random call)
		"""
		return randint(1, 100) <= self.get_success_probability()

	def resolve(self):
		"""
		Check whether the run is successful or not,
		Make the player pay for his order.
		"""
		self.player.money -= self.get_cost()
		self.player.save()

		if self.is_successful():
			self.resolve_successful()
		else:
			self.resolve_failure()

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

	def get_cost(self):
		cost = RunOrder.LAUNCH_COST
		cost += RunOrder.BASE_COST * self.additional_percents
		if self.has_influence_bonus:
			cost -= RunOrder.INFLUENCE_BONUS
		return cost
