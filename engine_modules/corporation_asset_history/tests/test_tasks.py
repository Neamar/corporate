# -*- coding: utf-8 -*- 
from engine.testcases import EngineTestCase
from messaging.models import Message
from engine_modules.corporation.models import BaseCorporation


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

		self.c = self.g.corporation_set.get(base_corporation=self.bc)
		self.c2 = self.g.corporation_set.get(base_corporation=self.bc2)
		self.c3 = self.g.corporation_set.get(base_corporation=self.bc3)

		self.g.disable_invisible_hand = True


	def test_assets_saved_on_resolution(self):
		"""
		The game should save the corporation assets on resolution
		"""

		self.g.resolve_current_turn()
		self.assertEqual(self.c.assethistory_set.get(turn=1).assets, self.reload(self.c).assets)

	def test_task_generate_corporation_ranking(self):
		"""
		The game should write the ranking of every corporation
		"""		
		self.c3.assets = 13
		self.c3.save()
		self.c2.assets = 12
		self.c2.save()

		self.g.resolve_current_turn()
		message_content = self.p.message_set.get(flag=Message.RESOLUTION,turn=self.g.current_turn - 1).content

		expected="""1- Ares : 13  (+3)
2- Renraku : 12  (+2)
3- NC&T : 10  (+0)"""

		self.assertTrue(expected in message_content)
