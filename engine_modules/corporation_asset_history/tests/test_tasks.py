# -*- coding: utf-8 -*- 
from engine.testcases import EngineTestCase
from engine.models import Message
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
		self.last_corporation.assets = 7
		self.last_corporation.save()

		self.medium_corporation = self.g.corporation_set.get(base_corporation=self.bc2)
		self.medium_corporation.assets = 10
		self.last_corporation.save()

		self.first_corporation = self.g.corporation_set.get(base_corporation=self.bc3)
		self.first_corporation.assets = 13
		self.first_corporation.save() 

		setattr(self.g,'disable_invisible_hand',True)

	def test_AssetHistory(self):
		"""
		The game should have all the corporation assets saved at the end of the turn
		"""
		nb_corporation=Corporation.objects.filter(game=self.g).count()
		self.g.save()
		self.g.resolve_current_turn()
		nb_corporation_saved=AssetHistory.objects.filter(turn=1).count()
		self.assertEqual(nb_corporation,nb_corporation_saved)
		"""
		Test the corporate classement note content
		"""
		self.last_corporation.assets = 13
		self.last_corporation.save()
		self.medium_corporation.assets = 12
		self.medium_corporation.save()
		self.first_corporation.assets = 10
		self.first_corporation.save() 

		self.g.resolve_current_turn()
		message_content=Message.objects.filter(flag=Message.GLOBAL_NOTE,title="Classement corporatiste").order_by('-pk')[0].content
		expected="1- NC&T : 13  (+6)\n2- Renraku : 12  (+2)\n3- Ares : 10  (-3)\n"
		self.assertEqual(message_content,expected)


