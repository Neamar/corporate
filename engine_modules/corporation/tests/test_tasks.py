from engine.testcases import EngineTestCase


class CrashCorporationTaskTest(EngineTestCase):

	def test_corporation_crashed_when_market_assets_drop_to_zero(self):
		"""
		Corporations should crash when their market assets drop to 0
		"""

		self.c.set_market_assets(0)
		self.c.save()

		self.g.resolve_current_turn()

		corporation = self.reload(self.c)
		self.assertEqual(corporation.crash_turn, self.g.current_turn - 1)

	def test_corporation_crashed_when_assets_drop_to_zero(self):
		"""
		Corporations should actually crash as soon as their assets drop to 0
		This is a different test from test_corporation_deleted_when_market_assets_drop_to_zero, because we have to take the MarketBubbles into account
		"""

		corporation_markets = self.c.corporation_markets

		for cm in corporation_markets:
			if self.c.assets > 0:
				# because a market cannot be negative, this ensures that at the end, Corporation's assets will be exactly 0
				# unfortunately, because bubbles are only computed in resolve_current_turn, this also ensures that each market has value 0 ...
				corporation_market = self.c.corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
				self.c.update_assets(delta=-self.c.assets, corporation_market=corporation_market)
			cm.save()

		self.g.resolve_current_turn()

		corporation = self.reload(self.c)
		self.assertEqual(corporation.crash_turn, self.g.current_turn - 1)

	def test_corporation_not_deleted_when_assets_not_zero(self):
		"""
		A corporation should not crash when it has one market asset at 0 but not its assets
		"""

		corporation_market = self.c.get_random_corporation_market()
		corporation_market.value = 100
		corporation_market.save()

		negative_corporation_market = self.c.get_random_corporation_market()
		while negative_corporation_market == corporation_market:
			negative_corporation_market = self.c.get_random_corporation_market()

		negative_corporation_market.value = -10
		negative_corporation_market.save()

		self.reload(self.c)

	def test_phoenix_crash(self):
		"""
		Test that Taurus crash the first time applying it's first_effect and crash the second time without appling it
		corporation c3 is taurus (file named in date/cities/test/taurus.md)
		"""
		self.c3.set_market_assets(0)
		self.c3.save()

		self.g.resolve_current_turn()

		# test that corporation disn't crash the first time
		self.assertEqual(self.reload(self.c3).crash_turn, None)
		# test that corporation assets are correct
		self.assertEqual(self.reload(self.c3).assets, 6)  # crash effect is +6

		self.c3.set_market_assets(0)
		self.c3.save()

		self.g.resolve_current_turn()

		# test that corporation disn't crash the second time time
		self.assertEqual(self.reload(self.c3).crash_turn, self.g.current_turn - 1)
		# test that corporation assets are correct
		self.assertEqual(self.reload(self.c3).assets, 0)

	def test_phoenix_violent_crash(self):
		"""
		test that Taurus will crash if the +6 bonus is not enough
		"""
		self.c3.set_market_assets(-7)
		self.c3.save()

		self.g.resolve_current_turn()

		# test that corporation disn't crash the first time
		self.assertEqual(self.reload(self.c3).crash_turn, self.g.current_turn - 1)
		# test that corporation assets are correct
		self.assertEqual(self.reload(self.c3).assets, -1)
