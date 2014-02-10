from django.db import IntegrityError

from engine.testcases import EngineTestCase
from engine.models import Game, Player
from messaging.models import Message, Note


class ModelTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def test_message_author_game_equals_player_game(self):
		"""
		Check if author's game = player's game
		"""

		p2 = Player(game=self.g)
		p2.save()

		g2 = Game()
		g2.save()

		p3 = Player(game=g2)
		p3.save()

		m = Message(title="titre", author=self.p, turn=self.g.current_turn)
		m.save()
		m.recipient_set.add(p2)
		m.save()

		m2 = Message(title="titre1", author=self.p, turn=self.g.current_turn)
		m2.save()
		
		self.assertRaises(IntegrityError, lambda: m2.recipient_set.add(p3))

	def test_message_building_content(self):
		"""
		Check if the content is built properly
		"""
		Note.objects.create(
			category="T1",
			content="C1",
			turn=self.g.current_turn
		)
		Note.objects.create(
			category="T2",
			content="C3",
			turn=self.g.current_turn
		)
		Note.objects.create(
			category="T1",
			content="C2",
			turn=self.g.current_turn
		)

		opening = "Opening"
		ending = "Ending"
		m = Message.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=Note.objects.all(),
			opening=opening,
			ending=ending,
			title="test",
			turn=self.g.current_turn
		)

		expected = """Opening

## T1
* C1
* C2

## T2
* C3

Ending
"""
		self.assertEquals(m.content, expected)
