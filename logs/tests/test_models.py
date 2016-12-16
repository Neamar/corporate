# -*- coding: utf-8 -*-
import json
from engine.testcases import EngineTestCase
from logs.models import Log
from engine.models import Game


class LogTest(EngineTestCase):
	def setUp(self):
		super(LogTest, self).setUp()

		self.l = Log(
			turn=1,
			game=self.g,
			delta=1,
			hide_for_players=False,
			public=True,
			event_type=Game.OPE_PROTECTION,
			data=json.dumps({
				"player": "testplayer",
				"market": "testmarket",
				"corporation": "testcorporation"
			}),
			corporation=self.c,
			corporation_market=self.c.get_random_corporation_market()
		)

		self.l.save()

	def test_log_display(self):
		"""
		Logs should be displayed properly, according to parameters
		"""
		self.assertEqual(self.l.get_display(display_context="player", is_personal=True), u"<p>Vous avez lancé une opé de protection sur le marché testmarket de testcorporation</p>")

		self.assertEqual(self.l.get_display(display_context="corporation", is_personal=False), u"<p>testplayer a lancé une opé de protection sur le marché testmarket</p>")

	def test_logs_retrieval_for_player(self):
		pass
