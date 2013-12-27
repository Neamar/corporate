from engine.testcases import EngineTestCase
from engine_modules.invisible_hand import InvisibleHand
from engine_modules.corporation import Corporation, BaseCorporation

class TaskTest(EngineTestCase):
	"""
	Unit tests for invisible_hand task
	"""
	def test_invisible_hand(self):
		bc = BaseCorporation(name="bc1")
		bc.save()

		bc2 = BaseCorporation(name="bc2")
		bc2.save()

		c = Corporation(base_corporation=bc, game=self.g, assets=10)
		c.save()

		c2 = Corporation(base_corporation=bc2, game=self.g, assets=15)
		c2.save()

		InvisibleHand.run(self.g)
		c = c.reload()
		c2 = c2.reload()
		
		self.assertNotEqual(c.assets, 10)
		self.assertNotEqual(c2.assets, 15)
		self.assertEqual(c.assets + c2.assets, 25)
