from django.core.exceptions import ValidationError
from django.dispatch import receiver

from engine.testcases import EngineTestCase
from engine_modules.citizenship.models import CitizenshipOrder
from engine_modules.share.models import Share
from engine.dispatchs import game_event


class SignalsTest(EngineTestCase):
	def setUp(self):

		super(SignalsTest, self).setUp()

		self.s = Share(
			player=self.p,
			corporation=self.c
		)
		self.s.save()

		self.o = CitizenshipOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.clean()
		self.o.save()

	def test_cant_create_order_twice(self):
		"""
		Order can't be created twice
		"""
		o2 = CitizenshipOrder(
			player=self.p,
			corporation=self.c
		)

		self.assertRaises(ValidationError, o2.clean)

	def test_cant_get_citizenship_without_share(self):
		"""
		You need at least one share to get citizenship
		"""
		self.s.delete()
		self.o.delete()
		self.assertRaises(ValidationError, self.o.clean)

	def test_get_citizenship_second_time_create_remove_citizenship_event(self):
		"""
		When you already have a citizenship and you change it, two events must be triggered
		"""
		# New turn because you can't change your citizenship twice in same turn
		self.g.resolve_current_turn()

		# create the function that will catch the signal
		@receiver(game_event)
		def catch_game_event(sender, instance, event_type, **kwargs):
			if event_type == 'ADD_CITIZENSHIP':
				self.g.add_citizenship_was_called = 1
			elif event_type == 'REMOVE_CITIZENSHIP':
				self.g.remove_citizenship_was_called = 1

		# Buy a share to have the new nationality
		self.s = Share(
			player=self.p,
			corporation=self.c2
		)
		self.s.save()

		# Change citizenship
		self.o = CitizenshipOrder(
			player=self.p,
			corporation=self.c2
		)
		self.o.clean()
		self.o.save()

		self.g.resolve_current_turn()

		self.assertEquals(self.g.add_citizenship_was_called, 1)
		self.assertEquals(self.g.remove_citizenship_was_called, 1)

		# disconnect receiver
		game_event.disconnect(catch_game_event)
