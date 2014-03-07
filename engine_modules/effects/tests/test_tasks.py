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
		self.update_effect(self.first_corporation, 'on_first', "corporations.get(base_corporation_slug='%s').update_assets(5)" % self.first_corporation.base_corporation_slug)
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
		self.update_effect(self.last_corporation, 'on_last', "corporations.get(base_corporation_slug='%s').update_assets(-5)" % self.last_corporation.base_corporation_slug)
		self.update_effect(self.first_corporation, 'on_first', "")

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.last_corporation).assets, initial_assets - 5)
