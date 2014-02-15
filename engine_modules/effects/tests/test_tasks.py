from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation


class TasksTest(EngineTestCase):
	def setUp(self):

		super(TasksTest, self).setUp()

		self.c.assets = 10
		self.c.save()
		self.medium_corporation = self.c

		self.c2.assets = 20
		self.c2.save()
		self.first_corporation = self.c2

		self.c3.assets = 5
		self.c3.save()
		self.last_corporation = self.c3

	def test_first_effect(self):
		"""
		Test that the first corporation's on_first effect gets applied
		"""

		# Change the default code
		base_first_corporation = self.first_corporation.base_corporation
		default_on_first = base_first_corporation.on_first

		test_first_effect = """
c = game.corporation_set.get(base_corporation_slug='%s')
c.assets=31337
c.save()
""" % self.first_corporation.base_corporation_slug

		base_first_corporation.on_first = base_first_corporation.compile_effect(test_first_effect, 'on_first')

		try:
			self.g.resolve_current_turn()
			self.assertEqual(self.reload(self.first_corporation).assets, 31337)
		except:
			raise
		finally:
			# Restore default behavior whatever happens
			base_first_corporation.on_first = default_on_first

	def test_last_effect(self):
		"""
		Test that the first corporation's on_last effect gets applied
		"""

		# Change the default code
		base_last_corporation = self.last_corporation.base_corporation
		default_on_last = base_last_corporation.on_last

		test_last_effect = """
c = game.corporation_set.get(base_corporation_slug='%s')
c.assets=337
c.save()
""" % self.first_corporation.base_corporation_slug

		base_last_corporation.on_last = base_last_corporation.compile_effect(test_last_effect, 'on_last')

		try:
			self.g.resolve_current_turn()
			self.assertEqual(self.reload(self.first_corporation).assets, 337)
		except:
			raise
		finally:
			# Restore default behavior whatever happens
			base_last_corporation.on_last = default_on_last
