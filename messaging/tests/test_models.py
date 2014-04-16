# -*- coding: utf-8 -*-
from django.db import IntegrityError

from engine.testcases import EngineTestCase
from engine.models import Game, Player
from messaging.models import Message, Note


class ModelsTest(EngineTestCase):
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
		Check content is built in right order
		"""

		Note.objects.create(
			content="global",
			turn=self.g.current_turn
		)
		Note.objects.create(
			category=Note.SPECULATION,
			content="speculation",
			turn=self.g.current_turn
		)
		Note.objects.create(
			category=Note.RUNS,
			content="runs",
			turn=self.g.current_turn
		)
		Note.objects.create(
			category=Note.DIVIDEND,
			content="dividend",
			turn=self.g.current_turn
		)

		opening = "Opening"
		m = Message.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=Note.objects.all(),
			opening=opening,
			title="test",
			turn=self.g.current_turn
		)

		expected = u"""Opening

* global

### Runs
* runs

### Spéculations
* speculation

### Dividendes
* dividend"""

		self.assertEqual(m.content.strip(), expected)
