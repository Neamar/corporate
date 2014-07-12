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
		This is run on the test city, without too many corporations, for faster tests.
		"""

		self.g = Game()
		# Disable all side effects for the game (first and last effects, invisible hand)
		self.g.disable_side_effects = True
		self.g.save()

		self.p = Player(game=self.g)
		self.p.save()
		self.initial_money = self.p.money

		self.c = self.g.corporations['c']
		self.c2 = self.g.corporations['c2']
		self.c3 = self.g.corporations['c3']

		# TODO: move to another place, in engine_modules/runs
		# TODO : add test for 90% restriction
		from engine_modules.run.models import RunOrder
		RunOrder.MAX_PERCENTS = 100

		from engine_modules.corporation_run.models import ProtectionOrder
		ProtectionOrder.MAX_PERCENTS = 100
