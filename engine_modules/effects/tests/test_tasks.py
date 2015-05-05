from engine.testcases import EngineTestCase
from engine_modules.corporation.decorators import override_base_corporations


class TasksTest(EngineTestCase):
	def setUp(self):

		super(TasksTest, self).setUp()

		self.c.market_assets = 20
		self.c.save()
		self.medium_corporation = self.c

		self.c2.market_assets = 40
		self.c2.save()
		self.first_corporation = self.c2

		self.c3.market_assets = 10
		self.c3.save()
		self.last_corporation = self.c3

		self.g.force_first_last_effects = True

	def update_effect(self, corporation, type, code):
		"""
		Update base_corporation code, for testing.
		"""
		base_corporation = corporation.base_corporation
		setattr(base_corporation, type, base_corporation.compile_effect(code, type))

	@override_base_corporations
	def test_first_effect(self):
		"""
		Test that the first corporation's on_first effect gets applied
		"""
		initial_assets = self.first_corporation.assets

		# Change the default code
		self.update_effect(self.first_corporation, 'on_first', "update('%s', 3)" % self.first_corporation.base_corporation_slug)
		self.update_effect(self.last_corporation, 'on_last', "")

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.first_corporation).assets, initial_assets + 3)

	@override_base_corporations
	def test_last_effect(self):
		"""
		Test that the first corporation's on_last effect gets applied
		"""
		initial_assets = self.last_corporation.assets

		# Change the default code
		self.update_effect(self.last_corporation, 'on_last', "update('%s', -3)" % self.last_corporation.base_corporation_slug)
		self.update_effect(self.first_corporation, 'on_first', "")

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.last_corporation).assets, initial_assets - 3)

	@override_base_corporations
	def test_first_effect_target_market(self):
		"""
		Test that the first corporation's on_first effect gets applied on specified market
		"""
		initial_assets = self.first_corporation.assets
		target_corporation_market = self.first_corporation.get_random_corporation_market()
		initial_target_assets = target_corporation_market.value

		# Change the default code
		self.update_effect(self.first_corporation, 'on_first', "update('%s', 3, market='%s')" % (self.first_corporation.base_corporation_slug, target_corporation_market.market.name))
		self.update_effect(self.last_corporation, 'on_last', "")

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.first_corporation).assets, initial_assets + 3)
		self.assertEqual(self.reload(target_corporation_market).value, initial_target_assets + 3)

	@override_base_corporations
	def test_update_create_assetdelta(self):
		"""
		Using update() function in code creates AssetDelta
		"""
		# Change the default code
		self.update_effect(self.last_corporation, 'on_last', "update('%s', -3)" % self.last_corporation.base_corporation_slug)
		self.update_effect(self.first_corporation, 'on_first', "")

		self.g.resolve_current_turn()
		asset_delta = self.last_corporation.assetdelta_set.get()
		self.assertEqual(asset_delta.category, asset_delta.EFFECT_LAST)
		self.assertEqual(asset_delta.delta, -3)
		self.assertEqual(asset_delta.corporation, self.last_corporation)

	@override_base_corporations
	def test_crashed_corporations(self):
		"""
		Test errors are gracefully handled when the corporation to affect does not exist anymore
		"""
		self.update_effect(self.last_corporation, 'on_last', "update('unknown_corporation', -5)")
		self.update_effect(self.first_corporation, 'on_first', "")

		# assertNoRaise
		self.g.resolve_current_turn()
