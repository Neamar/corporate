from engine.testcases import EngineTestCase
from engine.models import Game
from engine.dispatchs import post_create


class SignalTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def test_post_create_signal(self):
		"""
		Check is current_turn can't be greater than total_turn
		"""
		def first_creation(sender, instance, **kwargs):
			first_creation.was_called = True
		first_creation.was_called = False

		post_create.connect(first_creation)
		g2 = Game(total_turn=10)
		g2.save()
		self.assertTrue(first_creation.was_called)

		first_creation.was_called = False
		post_create.connect
		g2.current_turn += 1
		g2.save()
		# Should not be called again
		self.assertFalse(first_creation.was_called)

		post_create.disconnect(first_creation)
