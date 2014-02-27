# -*- coding: utf-8 -*-
from collections import Counter
from engine.tasks import ResolutionTask
from engine_modules.mdc.models import MDCVoteSession, MDCVoteOrder
from messaging.models import Newsfeed


class MDCVoteTask(ResolutionTask):
	"""
	Choose the MDC party line
	"""
	RESOLUTION_ORDER = 0
	ORDER_TYPE = MDCVoteOrder

	def run(self, game):
		orders = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn)
		votes = {}
		for t in MDCVoteOrder.MDC_PARTY_LINE_CHOICES:
			votes[t[0]] = 0

		for order in orders:
			votes[order.party_line] += order.get_weight()

		top_line = Counter(votes).most_common(2)
		# Default to NONE
		official_line = None
		try:
			if top_line[0][1] != top_line[1][1]:
				official_line = top_line[0][0]
		except IndexError:
			# Only one line voted for
			if len(top_line) != 0:
				official_line = top_line[0][0]

		s = MDCVoteSession(
			current_party_line=official_line,
			game=game,
			turn=game.current_turn + 1
		)
		s.save()

		if official_line is not None:
			game.add_newsfeed(category=Newsfeed.MDC_REPORT, content=u"La coalition du MDC pour ce tour a voté %s" % s.get_current_party_line_display())

tasks = (MDCVoteTask, )
