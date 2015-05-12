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

	def test_get_citizenship_first_time_does_not_create_remove_citizenship_event(self):
		"""
		When you get citizenship for the first time, you should only fire the event of add_citizenship
		"""

		# create the function that will catch the signal
		@receiver(game_event)
		def catch_game_event(sender, instance, event_type, **kwargs):
			if event_type == 'ADD_CITIZENSHIP':
				self.g.add_citizenship_was_called = 1
			elif event_type == 'REMOVE_CITIZENSHIP':
				self.g.remove_citizenship_was_called = 1

		# Change citizenship
		self.o = CitizenshipOrder(
			player=self.p,
			corporation=self.c
		)
		self.o.clean()
		self.o.save()

		self.g.resolve_current_turn()

		self.assertEquals(self.g.add_citizenship_was_called, 1)
		self.assertRaises(AttributeError, lambda: self.g.remove_citizenship_was_called)

		# disconnect receiver
		game_event.disconnect(catch_game_event)
