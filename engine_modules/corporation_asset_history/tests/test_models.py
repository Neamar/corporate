from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation
from engine_modules.corporation_asset_history.models import AssetHistory


class TasksTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless")
		self.bc.save()
		self.bc2 = BaseCorporation(name="Renraku", description="Priceless")
		self.bc2.save()
		self.bc3 = BaseCorporation(name="Ares", description="Ruthless")
		self.bc3.save()

		super(TasksTest, self).setUp()

	def test_assets_saved_on_init(self):
		"""
		The game should save the corporation value on start
		"""
		nb_corporation = self.g.corporation_set.count()
		nb_assets_saved = AssetHistory.objects.count()
		self.assertEqual(nb_corporation, nb_assets_saved)


	def test_assets_saved_on_resolution(self):
		"""
		The game should save the corporation value on resolution
		"""
		nb_corporation = self.g.corporation_set.count()
		self.g.resolve_current_turn()

		nb_assets_saved = AssetHistory.objects.count()
		self.assertEqual(nb_corporation * 2, nb_assets_saved)
