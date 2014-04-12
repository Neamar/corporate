from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ExtractionOrder


class SignalsTest(EngineTestCase):
	def setUp(self):

		super(SignalsTest, self).setUp()

	def test_datasteal_target_stealer_different(self):
		"""
		Target and stealer must be different for Datasteal.
		"""

		self.dso = DataStealOrder(
			player=self.p,
			target_corporation=self.c,
			stealer_corporation=self.c
		)

		self.assertRaises(ValidationError, self.dso.clean)

	def test_extraction_target_stealer_different(self):
		"""
		Target and stealer must be different for Extraction.
		"""

		self.dso = ExtractionOrder(
			player=self.p,
			target_corporation=self.c,
			kidnapper_corporation=self.c
		)

		self.assertRaises(ValidationError, self.dso.clean)
