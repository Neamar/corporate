from django.test import TestCase as DjangoTestCase
from engine.models import Game, Player


class TestCase(DjangoTestCase):
	"""
	Add a convenience method to reload an item from DB
	"""

	def reload(self, item):
		"""
		Reload an item from DB
		"""
		return item.__class__.objects.get(pk=item.pk)


class EngineTestCase(TestCase):
	"""
	Base class for unittesting engine.
	Add a game in self.g and a player in self.p
	"""

	def setUp(self):
		"""
		Setup initial configuration.
		For faster tests, remove all BaseCorporation to avoid creating useless fixtures.
		"""

		from engine_modules.corporation.models import BaseCorporation
		original_base_corporations = BaseCorporation.base_corporations
		try:
			BaseCorporation.base_corporations = {}

			self.initial_money = Player._meta.get_field_by_name('money')[0].default
			self.g = Game()
			self.g.save()
			self.p = Player(game=self.g, money=self.initial_money)
			self.p.save()
		except:
			raise
		finally:
			BaseCorporation.base_corporations = original_base_corporations
