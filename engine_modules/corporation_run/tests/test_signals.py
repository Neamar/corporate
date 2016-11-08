from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
from engine_modules.corporation_run.models import DataStealOrder, ExtractionOrder, SabotageOrder, ProtectionOrder


class SignalsTest(EngineTestCase):
	def setUp(self):
		super(SignalsTest, self).setUp()

		# We disable the test that stop you from start more than one run on the same target
		self.g.allow_several_runs_on_one_target = True

		common_corporation_market = self.c.get_common_corporation_market(self.c2)

		self.dso = DataStealOrder(
			player=self.p,
			target_corporation_market=common_corporation_market,
			stealer_corporation=self.c2,
		)
		self.dso.save()

		common_corporation_market = self.c.get_common_corporation_market(self.c2)

		self.eo = ExtractionOrder(
			player=self.p,
			target_corporation_market=common_corporation_market,
			stealer_corporation=self.c2,
		)
		self.eo.save()

		self.so = SabotageOrder(
			player=self.p,
			target_corporation_market=common_corporation_market,
			additional_percents=0,
		)
		self.so.clean()
		self.so.save()

		self.po = ProtectionOrder(
			player=self.p,
			protected_corporation_market=self.eo.target_corporation_market,
			hidden_percents=10,
		)
		self.po.clean()
		self.po.save()

	def get_unique_market_for_corporation(self, corporation):
		return corporation.corporationmarket_set.get(market__name=corporation.base_corporation.markets.keys()[-1], turn=self.g.current_turn)

	def test_datasteal_target_stealer_different(self):
		"""
		Target and stealer must be different for Datasteal.
		"""
		self.dso.stealer_corporation = self.c
		self.assertRaises(OrderNotAvailable, self.dso.clean)

	def test_extraction_target_stealer_different(self):
		"""
		Target and stealer must be different for Extraction.
		"""
		self.eo.stealer_corporation = self.c
		self.assertRaises(OrderNotAvailable, self.eo.clean)

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

	def test_datasteal_negative_market(self):
		"""
		Target market must have positive assets
		"""
		target_corporation_market = self.dso.target_corporation_market
		target_corporation_market.value = -1
		target_corporation_market.save()
		# Stealer must have market assets lower than target
		stealer_corporation_market = self.dso.stealer_corporation.corporationmarket_set.get(market=target_corporation_market.market, turn=self.g.current_turn)
		stealer_corporation_market.value = -2
		stealer_corporation_market.save()
		self.assertRaises(OrderNotAvailable, self.dso.clean)

	def test_extraction_negative_market(self):
		"""
		Target market must have positive assets
		"""
		target_corporation_market = self.eo.target_corporation_market
		target_corporation_market.value = -1
		target_corporation_market.save()
		# Stealer must have market assets lower than target
		stealer_corporation_market = self.eo.stealer_corporation.corporationmarket_set.get(market=target_corporation_market.market, turn=self.g.current_turn)
		stealer_corporation_market.value = -2
		stealer_corporation_market.save()
		self.assertRaises(OrderNotAvailable, self.eo.clean)

	def test_sabotage_negative_market(self):
		"""
		Target market must have positive assets
		"""
		target_corporation_market = self.so.target_corporation_market
		target_corporation_market.value = -1
		target_corporation_market.save()
		self.assertRaises(OrderNotAvailable, self.so.clean)

	def test_protection_negative_market(self):
		"""
		Target market must have positive assets
		"""
		target_corporation_market = self.po.protected_corporation_market
		target_corporation_market.value = -1
		target_corporation_market.save()
		self.assertRaises(OrderNotAvailable, self.po.clean)

	def test_several_run_on_same_target_fail(self):
		"""
		Only one run is allowed by target. allow_several_runs_on_one_target is set on True on the test_models.py of corporation_run
		We used this variable because there are a lot of randoms corporations in the targets for testing
		"""
		self.g.allow_several_runs_on_one_target = False

		common_corporation_market = self.c.get_common_corporation_market(self.c2)
		self.so2 = SabotageOrder(
			player=self.p,
			target_corporation_market=common_corporation_market,
			additional_percents=0,
		)
		self.so2.save()
		self.assertRaises(OrderNotAvailable, self.po.clean)
