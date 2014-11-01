from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ExtractionOrder


class SignalsTest(EngineTestCase):
	def setUp(self):
		super(SignalsTest, self).setUp()
		self.dso = DataStealOrder(
			player=self.p,
			target_corporation_market=self.c.historic_corporation_market,
			stealer_corporation=self.c2,
		)
		self.dso.save()

		self.eo = ExtractionOrder(
			player=self.p,
			target_corporation_market=self.c.historic_corporation_market,
			stealer_corporation=self.c2,
		)
		self.eo.save()

	def get_unique_market_for_corporation(self, corporation):
		return corporation.corporationmarket_set.get(market__name=corporation.base_corporation.markets.keys()[-1])

	def test_datasteal_target_stealer_different(self):
		"""
		Target and stealer must be different for Datasteal.
		"""
		self.dso.stealer_corporation = self.c
		self.assertRaises(ValidationError, self.dso.clean)

	def test_extraction_target_stealer_different(self):
		"""
		Target and stealer must be different for Extraction.
		"""
		self.eo.stealer_corporation = self.c
		self.assertRaises(ValidationError, self.eo.clean)

	def test_datasteal_unavailable_market_for_stealer(self):
		"""
		Datasteal should not be able to target a corporation that doesn't
		have assets in the target market
		"""
		self.dso.target_corporation_market = self.get_unique_market_for_corporation(self.c)

		self.assertRaises(ValidationError, self.dso.clean)

	def test_datasteal_unavailable_market_for_target(self):
		"""
		Datasteal should not be able to target a corporation that doesn't
		have assets in the target market
		"""
		self.dso.target_corporation_market = self.get_unique_market_for_corporation(self.c2)

		self.assertRaises(ValidationError, self.dso.clean)

	def test_extraction_unavailable_market(self):
		"""
		Extraction should not be able to target a corporation that doesn't
		have assets in the target market
		"""
		self.eo.target_corporation_market = self.get_unique_market_for_corporation(self.c)

		self.assertRaises(ValidationError, self.eo.clean)

	def test_datasteal_stealer_above_target(self):
		"""
		A datasteal cannot be launched against a corporation that is
		(strictly) below the stealer on the target market
		"""

		self.dso.target_corporation_market.value = 0
		self.dso.target_corporation_market.save()

		self.assertRaises(ValidationError, self.dso.clean)

	def test_extraction_stealer_above_target(self):
		"""
		An extraction cannot be launched against a corporation that is
		(strictly) below the stealer on the target market
		"""

		self.eo.target_corporation_market.value = 0
		self.eo.target_corporation_market.save()

		self.assertRaises(ValidationError, self.eo.clean)
