# -*- coding: utf-8 -*-
from collections import Counter
from engine.tasks import ResolutionTask
from engine_modules.mdc.models import MDCVoteSession, MDCVoteOrder
from messaging.models import Newsfeed


class MDCVoteTask(ResolutionTask):
	"""
	Choose the MDC party line, and save it in an MDCVoteSession
	"""
	RESOLUTION_ORDER = 100
	ORDER_TYPE = MDCVoteOrder

	def run(self, game):
		orders = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn)
		votes = {}
		for t in MDCVoteOrder.MDC_PARTY_LINE_CHOICES:
			votes[t[0]] = 0

		for order in orders:
			votes[order.party_line] += order.get_weight()

		top_line = Counter(votes).most_common(2)
		# Default to None
		official_line = None
		try:
			if top_line[0][1] != top_line[1][1]:
				official_line = top_line[0][0]
		except IndexError:
			# Only one line voted for
			if len(top_line) != 0:
				official_line = top_line[0][0]

		s = MDCVoteSession(
			party_line=official_line,
			game=game,
			turn=game.current_turn + 1
		)
		s.save()

		if official_line is not None:
			game.add_newsfeed(category=Newsfeed.MDC_REPORT, content=u"La coalition du MDC pour ce tour a voté %s" % s.get_party_line_display())


class MDCLineCPUBTask(ResolutionTask):
	"""
	Enforce the effects of the MDC CPUB party line
	"""

	# Resolve after MDCVoteTask
	RESOLUTION_ORDER = 300

	def run(self, game):
		# Because this is run the turn of the vote, we have to ask for the next line, not the current one
		party_line = game.get_mdc_party_line(turn=game.current_turn + 1)

		if party_line != MDCVoteOrder.CPUB:
			return

		win_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn, party_line=MDCVoteOrder.CPUB)
		for o in win_votes:
			for c in o.get_friendly_corporations():
				c.update_assets(1)

		loss_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn, party_line=MDCVoteOrder.DEVE)
		for o in loss_votes:
			for c in o.get_friendly_corporations():
				c.update_assets(-1)


class MDCLineDEVETask(ResolutionTask):
	"""
	Enforce the effects of the MDC DEVE party line
	"""

	# Resolve after MDCVoteTask
	RESOLUTION_ORDER = 300

	def run(self, game):

		# Because this is ran the turn of the vote, we have to watch out for the next line
		party_line = game.get_mdc_party_line(turn=game.current_turn + 1)

		if party_line != MDCVoteOrder.DEVE:
			return

		win_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn, party_line=MDCVoteOrder.DEVE)
		for o in win_votes:
			for c in o.get_friendly_corporations():
				c.update_assets(1)

		loss_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn, party_line=MDCVoteOrder.CPUB)
		for o in loss_votes:
			for c in o.get_friendly_corporations():
				c.update_assets(-1)


tasks = (MDCVoteTask, MDCLineCPUBTask, MDCLineDEVETask)
