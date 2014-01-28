# -*- coding: utf-8 -*- 
from engine.testcases import EngineTestCase
from messaging.models import Message
from engine_modules.corporation.models import Corporation


class TasksTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		super(TasksTest, self).setUp()

		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='shiawase', assets=10)
		self.c2 = Corporation(base_corporation_slug='renraku', assets=10)
		self.c3 = Corporation(base_corporation_slug='ares', assets=10)
		self.g.corporation_set.add(self.c, self.c2, self.c3)

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
		message = self.p.message_set.get(flag=Message.RESOLUTION,turn=self.g.current_turn - 1)

		expected="""## Classement corporatiste
* 1- Ares Macrotechnology Incorporated : 13  (+3)
2- Renraku Computer Systems : 12  (+2)
3- Shiawase Corporation : 10  (+0)"""

		print message.content
		self.assertTrue(expected in message.content)
