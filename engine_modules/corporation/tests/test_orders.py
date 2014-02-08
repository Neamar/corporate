from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation


class ModelTest(EngineTestCase):
	def setUp(self):

		super(ModelTest, self).setUp()
		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='shiawase', assets=10)
		self.g.corporation_set.add(self.c)
		self.c2 = Corporation(base_corporation_slug='renraku', assets=10)
		self.g.corporation_set.add(self.c2)

		self.g.disable_invisible_hand = True

	def test_corporation_deleted_when_asset_drops_to_zero(self):
		"""
		Corporation should crash when their assets are null
		"""
		
		self.c.assets = 0
		self.c.save()

		self.g.resolve_current_turn()

		self.assertRaises(Corporation.DoesNotExist, lambda: self.reload(self.c))
