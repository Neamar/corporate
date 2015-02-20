from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation


class CrashCorporationTaskTest(EngineTestCase):
	def test_corporation_deleted_when_asset_drops_to_zero(self):
		"""
		Corporation should crash when their assets are null
		"""

		self.c.assets = 0
		self.c.save()

		self.g.resolve_current_turn()

		self.assertRaises(Corporation.DoesNotExist, lambda: self.reload(self.c))
