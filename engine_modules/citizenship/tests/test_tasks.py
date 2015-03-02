from engine.testcases import EngineTestCase
from engine_modules.citizenship.models import CitizenShipOrder


class CitizenshipTaskTest(EngineTestCase):
	def setUp(self):
		super(CitizenshipTaskTest, self).setUp()

		self.o = CitizenShipOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.save()

	def test_tasks_applied(self):
		"""
		The new player should have a citizenship in the new corporation
		"""
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.p).citizenship.corporation, self.c)
