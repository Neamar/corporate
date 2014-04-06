from engine.testcases import EngineTestCase
from engine_modules.corporation.testcases import override_base_corporations


class TasksTest(EngineTestCase):
	def setUp(self):

		super(TasksTest, self).setUp()

		self.c.assets = 20
		self.c.save()
		self.medium_corporation = self.c

		self.c2.assets = 40
		self.c2.save()
		self.first_corporation = self.c2

		self.c3.assets = 10
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
		self.update_effect(self.first_corporation, 'on_first', "update('%s', 5)" % self.first_corporation.base_corporation_slug)
		self.update_effect(self.last_corporation, 'on_last', "")

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.first_corporation).assets, initial_assets + 5)

	@override_base_corporations
	def test_last_effect(self):
		"""
		Test that the first corporation's on_last effect gets applied
		"""
		initial_assets = self.last_corporation.assets

		# Change the default code
		self.update_effect(self.last_corporation, 'on_last', "update('%s', -5)" % self.last_corporation.base_corporation_slug)
		self.update_effect(self.first_corporation, 'on_first', "")

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.last_corporation).assets, initial_assets - 5)

	@override_base_corporations
	def test_update_create_assetdelta(self):
		"""
		Using update() function in code creates AssetDelta
		"""
		# Change the default code
		self.update_effect(self.last_corporation, 'on_last', "update('%s', -5)" % self.last_corporation.base_corporation_slug)
		self.update_effect(self.first_corporation, 'on_first', "")

		self.g.resolve_current_turn()
		asset_delta = self.last_corporation.assetdelta_set.get()
		self.assertEqual(asset_delta.category, asset_delta.EFFECT_LAST)
		self.assertEqual(asset_delta.delta, -5)
		self.assertEqual(asset_delta.corporation, self.last_corporation)

	@override_base_corporations
	def test_crashed_corporations(self):
		"""
		Test errors are gracefully handled whe the corporation to affect does not exist anymore
		"""
		self.update_effect(self.last_corporation, 'on_last', "update('unknown_corporation', -5)")
		self.update_effect(self.first_corporation, 'on_first', "")

		# assertNoRaise
		self.g.resolve_current_turn()
