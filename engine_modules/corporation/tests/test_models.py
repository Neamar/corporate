from os import listdir

from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation, BASE_CORPO_DIR


class ModelTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation("renraku")

		super(ModelTest, self).setUp()

	def test_corporation_auto_created(self):
		"""
		Corporation should have been created alongside the game
		"""

		corporations = Corporation.objects.all()
		self.assertEqual(len(corporations), len([f for f in listdir(BASE_CORPO_DIR) if f.endswith('.md')]))

	def test_corporation_deleted_when_asset_drops_to_zero(self):
		"""
		Corporation should crash when their assets are null
		"""
		
		c = Corporation.objects.all()[0]
		c.assets = 0
		c.save()

		self.assertRaises(Corporation.DoesNotExist, lambda: self.reload(c))

	def test_corporation_deleted_when_asset_drops_below_zero(self):
		"""
		Corporation should crash when their assets drops below 0, without raising IntegrityError.
		"""

		c = Corporation.objects.all()[0]
		c.assets = -1
		c.save()

		self.assertRaises(Corporation.DoesNotExist, lambda: self.reload(c))
