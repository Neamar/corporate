# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from random import randint

from engine.models import Order


class RunOrder(Order):
	"""
	Base model for all runs
	"""
	BASE_COST = 50
	INFLUENCE_BONUS = 30

	has_influence_bonus = models.BooleanField(default=False, help_text="Accorder à cette run un bonus de 30% gratuit")
	additional_percents = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(9), MinValueValidator(1)], help_text="Palier de 10% supplémentaires.")
	hidden_percents = models.SmallIntegerField(default=0, editable=False)

	def clean(self):
		super(RunOrder, self).clean()

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = 0
		if self.has_influence_bonus:
			proba += 30
		proba += self.additional_percents * 10

		proba += self.hidden_percents * 10
		return proba

	def is_successful(self):
		"""
		Return true if the run is is_successful (random call)
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
		return RunOrder.BASE_COST * self.additional_percents

	def repay(self):
		"""
		Give the player back half the money he paid
		"""
		self.player.money += self.get_cost() / 2
		self.player.save()
