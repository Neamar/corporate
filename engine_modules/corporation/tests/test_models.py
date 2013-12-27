from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation


class ModelTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless.")
		self.bc.save()

		super(ModelTest, self).setUp()

	def test_corporation_auto_created(self):
		"""
		Corporation should have been created alongside the game
		"""
		corporations = Corporation.objects.all()
		self.assertEqual(len(corporations), 1)
		self.assertEqual(corporations[0].base_corporation, self.bc)

	def test_corporation_deleted_when_asset_drops_below_zero(self):
		"""
		Corporation should have been created alongside the game
		"""
		c = Corporation.objects.all()[0]
		c.assets = -1
		c.save()

		self.assertRaises(Corporation.DoesNotExist, lambda: self.reload(c))
