from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation


class ModelTest(EngineTestCase):
	def setUp(self):

		super(ModelTest, self).setUp()

	def test_corporation_auto_created(self):
		"""
		Corporation should have been created alongside the game
		"""

		corporations = Corporation.objects.all()
		self.assertEqual(len(corporations), len(BaseCorporation.retrieve_all()))
