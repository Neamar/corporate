from engine.testcases import EngineTestCase
from engine_modules.corporation.models import AssetDelta
from engine_modules.corporation.decorators import override_base_corporations


class TaskTest(EngineTestCase):
	def setUp(self):

		super(TaskTest, self).setUp()
		self.g.force_bubbles = True

	def update_effect(self, corporation, type, code):
		"""
		Update base_corporation code, for testing.
		"""
		base_corporation = corporation.base_corporation
		setattr(base_corporation, type, base_corporation.compile_effect(code, type))

	def test_positive_bubble_increase_assets(self):
		"""
		A corporation with a domination (so positive bubble) should see its assets augmented by 1
		WARNING: this test only works on the prerequisite that every corporation has one and only one corporation-specific Market and that all markets have the same value.
		"""

		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets
		begin_assets_3 = self.c3.assets

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, begin_assets_1 + 1)
		self.assertEqual(self.reload(self.c2).assets, begin_assets_2 + 1)
		self.assertEqual(self.reload(self.c3).assets, begin_assets_3 + 1)

	def test_positive_bubble_no_monopoly(self):
		"""
		A corporation with a domination should see its assets augmented by 1, even if there are competitors
		"""

		common_corporation_markets_1_2 = self.c.get_common_corporation_markets(self.c2)
		common_corporation_markets_1_3 = self.c.get_common_corporation_markets(self.c3)

		target_corporation_market = None
		for cm in common_corporation_markets_1_2:
			if cm in common_corporation_markets_1_3:
				target_corporation_market = cm

		corporation_market = self.c.corporationmarket_set.get(market=target_corporation_market.market, turn=self.g.current_turn)
		self.c.update_assets(delta=target_corporation_market.value, category=AssetDelta.RUN_DATASTEAL, corporationmarket=corporation_market)

		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets
		begin_assets_3 = self.c3.assets

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, begin_assets_1 + 2)
		self.assertEqual(self.reload(self.c2).assets, begin_assets_2 + 1)
		self.assertEqual(self.reload(self.c3).assets, begin_assets_3 + 1)

	def test_negative_bubble_decrease_assets(self):
		"""
		A corporation with a market_asset at 0 (so negative bubble) should see its assets diminished by 1
		"""

		begin_assets_1 = self.c.assets
		corporation_markets = self.c.corporation_markets
		markets_2 = self.c2.markets
		# The Market at 0 must be the one that is Corporation-specific, or there is also going to be a positive bubble
		cm = None
		for corporation_market in corporation_markets:
			if corporation_market.market not in markets_2:
				cm = corporation_market
		differential = cm.value
		# Should there be an AssetDelta for tests ?
		corporation_market = self.c.corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
		self.c.update_assets(delta=-differential, category=AssetDelta.RUN_DATASTEAL, corporationmarket=corporation_market)

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, begin_assets_1 - differential - 1)

	@override_base_corporations
	def test_bubbles_after_effects(self):
		"""
		Ensure bubbles are redistributed *after* first and last effect.
		This test is quite complicated, and quite specific: the first and last effects, in particular. Assets must be distributed as in the test before last.
		It tests a big part of the game's behavior, so it can break for a lot of reasons.
		"""

		self.g.force_first_last_effects = True
		corporation_markets = self.c.corporation_markets
		corporation_markets_2 = self.c2.corporation_markets
		target_corporation_market = None
		# Both target_corporation_market_1 and _2 must be corporation-specific, lest there also be a positive bubble on this market when there should only be a negative on another
		for corporation_market in corporation_markets:
			if corporation_market.market not in [cm.market for cm in corporation_markets_2]:
				target_corporation_market = corporation_market
				break
		else:
			raise Exception("Corporations share all their markets!")
		for corporation_market in corporation_markets_2:
			if corporation_market.market not in [cm.market for cm in corporation_markets]:
				target_corporation_market_2 = corporation_market
				break
		else:
			raise Exception("Corporations share all their markets!")

		# Beware: c and c2 must not crash !
		differential_1 = target_corporation_market.value
		differential_2 = target_corporation_market_2.value

		# Create a negative bubble, and make c last
		self.c.update_assets(delta=-differential_1, category=AssetDelta.RUN_DATASTEAL, corporationmarket=target_corporation_market)
		# Create a positive bubble, and make c2 first
		self.c2.update_assets(delta=differential_2, category=AssetDelta.INVISIBLE_HAND, corporationmarket=target_corporation_market_2)

		# c is last, its effects will be to minimize c2 own's market
		self.update_effect(self.c, 'on_last', "update('%s', %i, market='%s')" % (self.c2.base_corporation_slug, -2 * differential_2, target_corporation_market_2.market.name))
		# c2 is first, its effects will be to maximize c own's market
		self.update_effect(self.c2, 'on_first', "update('%s', %i, market='%s')" % (self.c.base_corporation_slug, 2 * differential_1, target_corporation_market.market.name))

		pre_bubbles_assets_1 = self.c.assets
		pre_bubbles_assets_2 = self.c2.assets
		pre_bubbles_assets_3 = self.c3.assets

		self.g.resolve_current_turn()

		# Here, we only expect a '+1' or a '-1' because there was no negative bubble in the DB (for turn 0, since we hardcoded our update_assets).
		self.assertEqual(self.reload(self.c).assets, pre_bubbles_assets_1 + 2 * differential_1 + 1)
		self.assertEqual(self.reload(self.c2).assets, pre_bubbles_assets_2 - 2 * differential_2 - 1)
		self.assertEqual(self.reload(self.c3).assets, pre_bubbles_assets_3 + 1)
