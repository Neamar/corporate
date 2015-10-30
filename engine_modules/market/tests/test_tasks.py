# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase
from engine_modules.corporation.decorators import override_base_corporations

from engine_modules.corporation.models import AssetDelta


class TaskTest(EngineTestCase):
	def setUp(self):

		super(TaskTest, self).setUp()
		self.g.force_bubbles = True
		self.g.save()

	def update_effect(self, corporation, type, code):
		"""
		Update base_corporation code, for testing.
		"""
		base_corporation = corporation.base_corporation
		setattr(base_corporation, type, base_corporation.compile_effect(code, type))

	def test_replicate_corporationmarket_task(self):
		"""
		Test that the CorporationMarkets are correct for different turns
		"""

		# For this test, we should disable bubbles
		del self.g.force_bubbles
		self.g.save()

		market = self.c.markets[0]
		corporation_market = self.c.corporationmarket_set.get(market=market, turn=0)
		t0_val = corporation_market.value
		corporation_market = self.c.corporationmarket_set.get(market=market, turn=self.g.current_turn)
		corporation_market.value = t0_val + 1
		corporation_market.save()
		self.g.resolve_current_turn()

		corporation_market = self.reload(self.c).corporationmarket_set.get(market=market, turn=1)
		t1_val = corporation_market.value
		corporation_market = self.c.corporationmarket_set.get(market=market, turn=self.g.current_turn)
		corporation_market.value = t1_val + 3
		corporation_market.save()
		self.g.resolve_current_turn()

		corporation_market = self.reload(self.c).corporationmarket_set.get(market=market, turn=2)
		t2_val = corporation_market.value

		self.assertEqual(t1_val, t0_val + 1)
		self.assertEqual(t2_val, t1_val + 3)

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
				break

		corporation_market = self.c.corporationmarket_set.get(market=target_corporation_market.market, turn=self.g.current_turn)
		self.c.update_assets(delta=target_corporation_market.value, category=AssetDelta.RUN_DATASTEAL, corporation_market=corporation_market)

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
				break
		differential = cm.value
		# Should there be an AssetDelta for tests ?
		corporation_market = self.c.corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
		self.c.update_assets(delta=-differential, category=AssetDelta.RUN_DATASTEAL, corporation_market=corporation_market)

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, begin_assets_1 - differential - 1)

	def test_positive_bubble_erased(self):
		"""
		A corporation that had a domination bubble whose assets in the Market then dropped below (or at the level of) another's should see its bubble removed
		"""

		# Resolve so that the bubble on the corporation-specific market is not taken into account
		self.g.resolve_current_turn()
		begin_assets_1 = self.reload(self.c).assets
		# The Market with a bubble must not be the one that is Corporation-specific, because that one has one anyway (unless it is 0, but then it has a negative bubble)
		cm = self.c.get_common_corporation_market(self.c2)
		differential = cm.value
		# This should be enough to get a domination bubble
		self.reload(self.c).update_assets(delta=differential, category=AssetDelta.RUN_DATASTEAL, corporation_market=cm)
		cm.save()

		self.g.resolve_current_turn()

		# Just to check that we do have a domination bubble
		self.assertEqual(self.reload(self.c).assets, begin_assets_1 + differential + 1)
		# We have to substract 1 more to counterbalance the bubble, which is taken into account
		self.reload(self.c).update_assets(delta=-differential - 1, category=AssetDelta.RUN_DATASTEAL, corporation_market=cm)
		cm.save()

		# Refresh the bubbles
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.c).assets, begin_assets_1)

	def test_negative_bubble_erased(self):
		"""
		A corporation that had a negative bubble whose assets in the Market then went up above 0 should see its bubble removed
		"""

		# Resolve so that the bubble on the corporation-specific market is not taken into account
		self.g.resolve_current_turn()
		begin_assets_1 = self.reload(self.c).assets
		# The Market with a bubble must not be the one that is Corporation-specific, because that one has one anyway (unless it is 0, but then it has a negative bubble)
		cm = self.c.get_common_corporation_market(self.c2)
		differential = cm.value
		# This should be enough to get a domination bubble
		self.reload(self.c).update_assets(delta=differential, category=AssetDelta.RUN_DATASTEAL, corporation_market=cm)

		self.g.resolve_current_turn()

		# Just to check that we do have a domination bubble
		self.assertEqual(self.reload(self.c).assets, begin_assets_1 + differential + 1)
		# We have to substract 1 more to counterbalance the bubble, which is taken into account
		self.reload(self.c).update_assets(delta=-differential - 1, category=AssetDelta.RUN_DATASTEAL, corporation_market=cm)
		cm.save()

		# Refresh the bubbles
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, begin_assets_1)

	def test_positive_bubbles_accounted_in_ranking(self):
		"""
		Positive Bubbles should give a bonus in the ranking, and it should count in assigning new bubbles.
		So a corporation with n assets on market m at turn t should have n+1 assets at turn t+1 and be ranked above a corporation
		with n assets, or on the same rank as a corporation with n+1 assets
		This test test bubble_value directly, so it is a bit more implementation-specific
		"""

		# Resolve so that the bubble on the corporation-specific market is not taken into account
		self.g.resolve_current_turn()
		# The Market with a bubble must not be the one that is Corporation-specific, because that one has one anyway (unless it is 0, but then it has a negative bubble)
		cm = self.c.get_common_corporation_market(self.c2)
		differential = 2
		# This should be enough to get a domination bubble
		self.reload(self.c).update_assets(delta=differential, category=AssetDelta.RUN_DATASTEAL, corporation_market=cm)

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(cm).bubble_value, 1)

		# This should NOT be enough to get a domination bubble
		cm2 = self.reload(self.c2).corporationmarket_set.get(turn=self.g.current_turn, market=cm.market)
		self.reload(self.c2).update_assets(delta=differential, category=AssetDelta.RUN_DATASTEAL, corporation_market=cm2)
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(cm).bubble_value, 1)
		# There should not be a bubble on c2's CorporationMarket
		self.assertEqual(self.reload(cm2).bubble_value, 0)

	def test_negative_bubble_disappears_at_zero(self):
		"""
		Negative Bubbles should be an incentive to get your Market assets back up to 0, because then your bubble disappears, and you get back up to 1 instead
		You then get a 2-increment boost instead of 1
		"""

		# Reevalutaion of the bubbles after the first/last effects should not have an effect but it could mask errors, so let's disable it
		self.g.disable_bubble_reevaluation = True
		self.g.save()

		corporation_markets = self.reload(self.c).corporation_markets
		markets_2 = self.c2.markets
		# The Market at 0 must be the one that is Corporation-specific, or there is also going to be a positive bubble
		cm = None
		for corporation_market in corporation_markets:
			if corporation_market.market not in markets_2:
				cm = corporation_market
				break
		differential = cm.value
		# Should there be an AssetDelta for tests ?
		corporation_market = self.reload(self.c).corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
		self.reload(self.c).update_assets(delta=-differential, category=AssetDelta.RUN_DATASTEAL, corporation_market=corporation_market)
		corporation_market.save()

		self.g.resolve_current_turn()
		corporation_market = self.reload(self.c).corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
		# There should now be a negative bubble on corporation_market
		begin_assets_1 = self.reload(self.c).assets
		# Get that corporation_market back up to 1
		self.reload(self.c).update_assets(delta=1, category=AssetDelta.RUN_DATASTEAL, corporation_market=corporation_market)
		self.g.resolve_current_turn()
		corporation_market = self.reload(self.c).corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
		# test that total assets equal to : begin assets + domination bubble (c is alone in this market) + bonus on that market + remove negative bubble
		self.assertEqual(self.reload(self.c).assets, begin_assets_1 + 1 + 1 + 1)
		self.assertEqual(self.reload(corporation_market).bubble_value, 1)

	def test_from_domination_to_negative(self):
		"""
		A corporation with a dominaion that then loses all its assets on the market, dropping it to 0
		should get a negative bubble and end up with a value of -1
		"""

		# Reevalutaion of the bubbles after the first/last effects should not have an effect but it could mask errors, so let's disable it
		self.g.disable_bubble_reevaluation = True
		self.g.save()

		corporation_markets = self.c.corporation_markets
		markets_2 = self.c2.markets
		# The Market at 0 must be the one that is Corporation-specific, or there is also going to be a positive bubble
		cm = None
		for corporation_market in corporation_markets:
			if corporation_market.market not in markets_2:
				cm = corporation_market
				break

		# Let's give that market a domination bubble. The value is arbitrary, if we want to make it safer, we could use the max_vals from AbstractBubblesTask
		self.g.resolve_current_turn()
		# Now that CorporationMarkets are per turn, we can't just reload: we have to requery the right object
		corporation_market = self.reload(self.c).corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)

		differential = self.reload(corporation_market).value
		begin_assets = self.reload(self.c).assets

		# Now take it away by dropping it down to 0
		self.reload(self.c).update_assets(delta=-differential, category=AssetDelta.RUN_DATASTEAL, corporation_market=corporation_market)
		self.g.resolve_current_turn()

		# -1 for losing a domination bubble, and -1 for getting a negative bubble
		corporation_market = self.reload(self.c).corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
		self.assertEqual(self.reload(self.c).assets, begin_assets - differential - 2)
		self.assertEqual(corporation_market.bubble_value, -1)

	def test_from_negative_to_domination_equality(self):
		"""
		If a corporation gets back up to 0 on a turn xhere another Corporation was dominating with a value of 1, these two corporations are tied.
		So none of them should get the domination bubble.
		"""

		# Reevalutaion of the bubbles after the first/last effects should not have an effect but it could mask errors, so let's disable it
		self.g.disable_bubble_reevaluation = True
		self.g.save()

		cm = self.reload(self.c).get_common_corporation_market(self.reload(self.c2))
		differential = cm.value
		# Let's drop the market to 0, so c gets a negative bubble
		self.reload(self.c).update_assets(delta=-differential, category=AssetDelta.RUN_DATASTEAL, corporation_market=cm)
		# We also have to drop c3 to 0, so it doesn't get in the way
		cm3 = self.c3.corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
		self.reload(self.c3).update_assets(delta=-cm3.value, category=AssetDelta.RUN_DATASTEAL, corporation_market=cm3)
		self.g.resolve_current_turn()

		# Now c2 should have a domination bubble, and c should have a negative bubble
		corporation_market = self.reload(self.c).corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
		corporation_market_2 = self.reload(self.c2).corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)

		self.assertEqual(corporation_market.bubble_value, -1)
		self.assertEqual(corporation_market_2.bubble_value, 1)

		# Bring c back up to 1, and c2 back down to 1
		self.reload(self.c).update_assets(delta=1, category=AssetDelta.RUN_DATASTEAL, corporation_market=corporation_market)
		self.reload(self.c2).update_assets(delta=-(corporation_market_2.value - 1), category=AssetDelta.RUN_DATASTEAL, corporation_market=corporation_market_2)

		self.g.resolve_current_turn()

		corporation_market = self.reload(self.c).corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
		corporation_market_2 = self.reload(self.c2).corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)

		self.assertEqual(corporation_market.bubble_value, 0)
		self.assertEqual(corporation_market_2.bubble_value, 0)

	@override_base_corporations
	def test_bubbles_after_effects(self):
		"""
		Ensure bubbles are redistributed *after* first and last effect.
		This test is quite complicated, and quite specific: the first and last effects, in particular. Assets must be distributed as in the test before last.
		It tests a big part of the game's behavior, so it can break for a lot of reasons.
		"""

		# Remove third corporation
		self.c3.delete()

		# Naturally, because we want to test with first/last effects, we have to enable them
		self.g.force_first_last_effects = True
		corporation_markets = self.c.corporation_markets
		corporation_markets_2 = self.c2.corporation_markets
		target_corporation_market = None
		# Both target_corporation_market_1 and _2 must be corporation-specific, let there also be a positive bubble on this market when there should only be a negative on another
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
		self.c.update_assets(delta=-differential_1, category=AssetDelta.RUN_DATASTEAL, corporation_market=target_corporation_market)
		# Create a positive bubble, and make c2 first
		self.c2.update_assets(delta=differential_2, category=AssetDelta.INVISIBLE_HAND, corporation_market=target_corporation_market_2)

		# c is last, its effects will be to minimize c2's own market
		self.update_effect(self.c, 'on_last', "update('%s', %i, market='%s')" % (self.c2.base_corporation_slug, -2 * differential_2, target_corporation_market_2.market.name))
		# c2 is first, its effects will be to maximize c's own market
		self.update_effect(self.c2, 'on_first', "update('%s', %i, market='%s')" % (self.c.base_corporation_slug, 2 * differential_1, target_corporation_market.market.name))

		pre_bubbles_assets_1 = self.reload(self.c).assets
		pre_bubbles_assets_2 = self.reload(self.c2).assets

		self.g.resolve_current_turn()

		# Here, we only expect a '+1' or a '-1' because there was no negative bubble in the DB (for turn 0, since we hardcoded our update_assets).
		self.assertEqual(self.reload(self.c).assets, pre_bubbles_assets_1 + 2 * differential_1 + 1)  # add positive bubble
		self.assertEqual(self.reload(self.c2).assets, pre_bubbles_assets_2 - 2 * differential_2 - 1)  # add negative bubble
