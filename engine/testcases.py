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

		# Create a Game, without creating all default base corporations
		from engine_modules.corporation.models import Corporation, BaseCorporation
		original_base_corporations = BaseCorporation.base_corporations
		BaseCorporation.base_corporations = {}
		try:
			self.g = Game()
			# Disable all side effects for the game (first and last effects, invisible hand)
			self.g.disable_side_effects = True
			self.g.save()
		except:
			raise
		finally:
			BaseCorporation.base_corporations = original_base_corporations

		# Create base corporations
		self.c = Corporation(base_corporation_slug='shiawase', assets=10)
		self.c2 = Corporation(base_corporation_slug='renraku', assets=10)
		self.c3 = Corporation(base_corporation_slug='ares', assets=10)
		self.g.corporation_set.add(self.c, self.c2, self.c3)

		self.p = Player(game=self.g)
		self.p.save()
		self.initial_money = self.p.money

		# TODO: move to another place, in engine_modules/runs
		# TODO : add test for 90% restriction
		from engine_modules.run.models import RunOrder
		RunOrder.MAX_PERCENTS = 100

		from engine_modules.corporation_run.models import ProtectionOrder
		ProtectionOrder.MAX_PERCENTS = 100
