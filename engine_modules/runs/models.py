# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator
from random import randint


class Run(models.Model):
	"""
	Base model for all runs
	"""

	has_influence_bonus = models.BooleanField(default=False, help_text="Accorder à cette run un bonus de 30% gratuit")
	additional_percents = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9)])

	def get_success_probability(self):
		"""
		Compute success probability, maxed by 90%
		"""
		proba = 0
		if self.has_influence_bonus:
			proba += 30
		proba += self.additional_percents * 10

		return min(90, proba)

	def is_successful(self):
		"""
		Return true if the run is is_successful (random call)
		"""
		return randint(0, 100) < self.get_success_probability()

	def resolve(self):
		raise NotImplementedError()

