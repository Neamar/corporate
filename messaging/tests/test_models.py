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

		g2 = Game(total_turn=20)
		g2.save()

		p3 = Player(game=g2)
		p3.save()

		m = Message(title="titre", author=self.p)
		m.save()
		m.recipient_set.add(p2)
		m.save()

		m2 = Message(title="titre1", author= self.p)
		m2.save()
		
		self.assertRaises(IntegrityError, lambda: m2.recipient_set.add(p3))

	def test_message_building_content(self):
		"""
		Check if the content is built properly
		"""
		Note.objects.create(
			category="T1",
			content="C1",
			is_global=False
		)
		Note.objects.create(
			category="T2",
			content="C3",
			is_global=False
		)
		Note.objects.create(
			category="T1",
			content="C2",
			is_global=False
		)

		opening="Opening"
		ending="Ending"
		m = Message.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=Note.objects.filter(is_global=False),
			opening=opening,
			ending=ending,
			title="test",
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

	def test_notes_removed(self):
		"""
		Notes should be removed after aggregation
		"""
		# n2 has been removed
		Note.objects.create(
			category="T1",
			content="C1",
			is_global=False
		)

		Message.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=Note.objects.filter(is_global=False),
			title="test",
		)

		self.assertEqual(Note.objects.filter(is_global=False).count(), 0)		
