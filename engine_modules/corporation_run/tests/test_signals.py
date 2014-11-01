from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ExtractionOrder


class SignalsTest(EngineTestCase):
	def setUp(self):

		super(SignalsTest, self).setUp()
		self.dso = DataStealOrder(
			player=self.p,
			target_corporation=self.c,
			stealer_corporation=self.c2,
			target_corporation_market=self.c.corporationmarket_set.get(market__name=self.c.historic_market.name)
		)
		self.dso.save()

		self.eo = ExtractionOrder(
			player=self.p,
			target_corporation=self.c,
			kidnapper_corporation=self.c2,
			target_corporation_market=self.c.corporationmarket_set.get(market__name=self.c.historic_market.name)
		)
		self.eo.save()

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
		self.eo.kidnapper_corporation = self.c
		self.assertRaises(ValidationError, self.eo.clean)

	def test_datasteal_unavailable_market(self):
		"""
		Datasteal should not be able to target a corporation that doesn't
		have assets in the target market
		"""

		# The last market is different in each test corporation
		self.dso.target_corporation_market = self.c.corporationmarket_set.get(
			market__name=self.c.base_corporation.markets.keys()[-1])

		self.assertRaises(ValidationError, self.dso.clean)

	def test_extraction_unavailable_market(self):
		"""
		Extraction should not be able to target a corporation that doesn't
		have assets in the target market
		"""

		# The last market is different in each test corporation
		self.eo.target_corporation_market = self.c.corporationmarket_set.get(
			market__name=self.c.base_corporation.markets.keys()[-1])

		self.assertRaises(ValidationError, self.eo.clean)

	def test_datasteal_stealer_above_target(self):
		"""
		A datasteal cannot be launched against a corporation that is
		(strictly) below the stealer on the target market
		"""

		target_corporation_market = self.dso.target_corporation.corporationmarket_set.get(market__name=self.dso.target_corporation_market.market.name)
		target_corporation_market.value = 0
		target_corporation_market.save()

		self.assertRaises(ValidationError, self.dso.clean)

	def test_extraction_stealer_above_target(self):
		"""
		An extraction cannot be launched against a corporation that is
		(strictly) below the stealer on the target market
		"""

		target_corporation_market = self.eo.target_corporation.corporationmarket_set.get(market__name=self.eo.target_corporation_market.market.name)
		target_corporation_market.value = 0
		target_corporation_market.save()

		self.assertRaises(ValidationError, self.eo.clean)
