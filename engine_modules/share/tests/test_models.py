from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation
from engine_modules.share.models import Share


class ModelTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation(name="NC&T", description="Reckless.")
		self.bc.save()

		super(ModelTest, self).setUp()

	def test_share_creation_automatically_set_turn(self):
		"""
		Share should be created at current turn
		"""
		s = Share(
			corporation=self.g.corporation_set.get(base_corporation=self.bc),
			player=self.p
		)
		s.save()

		self.assertEqual(s.turn, self.g.current_turn)
