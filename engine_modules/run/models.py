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

	has_influence_bonus = models.BooleanField(default=False, help_text="Accorder à cette run un bonus de 30% gratuit")
	additional_percents = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(9), MinValueValidator(1)])

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%

		It must be overriden.
		"""
		raise NotImplementedError()

	def is_successful(self):
		"""
		Return true if the run is is_successful (random call)
		"""
		return randint(1, 100) <= self.get_success_probability()

	def resolve(self):
		raise NotImplementedError()
		
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
