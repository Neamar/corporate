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
		Setup initial configuration
		"""
		self.initial_money = 1000
		self.g = Game(total_turn=10)
		self.g.save()
		self.p = Player(game=self.g, money=self.initial_money)
		self.p.save()