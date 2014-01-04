from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation,Corporation
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

		self.last_corporation = self.g.corporation_set.get(base_corporation=self.bc)
		self.last_corporation.assets -= 3
		self.last_corporation.save()

		self.medium_corporation = self.g.corporation_set.get(base_corporation=self.bc2)
		
		self.first_corporation = self.g.corporation_set.get(base_corporation=self.bc3)
		self.first_corporation.assets += 3
		self.first_corporation.save() 

	def test_qty_assets_savings(self):
		"""
		The game should have all the corporation assets saved at the end of the turn
		"""
		nb_corporation=Corporation.objects.filter(game=self.g).count()
		self.g.current_turn = 1
		self.g.save()
		self.g.resolve_current_turn()
		nb_corporation_saved=AssetHistory.objects.filter(turn=1).count()
		self.assertEqual(nb_corporation,nb_corporation_saved)

