# -*- coding: utf-8 -*-
from collections import Counter
from engine.tasks import ResolutionTask
from engine_modules.corporation.models import AssetDelta
from engine_modules.mdc.models import MDCVoteSession, MDCVoteOrder
from messaging.models import Newsfeed, Note


class MDCVoteTask(ResolutionTask):
	"""
	Choose the MDC party line, and save it in an MDCVoteSession
	"""
	RESOLUTION_ORDER = 100
	ORDER_TYPE = MDCVoteOrder

	def run(self, game):
		orders = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn)
		votes = {}
		for t in MDCVoteOrder.MDC_OPPOSITIONS.values():
			votes[t] = 0

		for order in orders:
			votes[order.coalition] += order.get_weight()
			order.player.add_note(category=Note.MDC, content="Vous avez rejoint la coalition *%s*." % order.get_coalition_display())

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
			coalition=official_line,
			game=game,
			turn=game.current_turn + 1
		)
		s.save()

		if official_line is not None:
			game.add_newsfeed(category=Newsfeed.MDC_REPORT, content=u"La coalition du MDC pour ce tour a voté %s" % s.get_coalition_display())

			# Message all player who voted for this line
			n = Note.objects.create(
				category=Note.MDC,
				content="Le MDC a suivi votre coalition.",
				turn=game.current_turn,
			)
			n.recipient_set = [order.player for order in orders if order.coalition == official_line]

			n = Note.objects.create(
				category=Note.MDC,
				content=u"Le MDC a rejoint la coalition opposée %s." % s.get_coalition_display(),
				turn=game.current_turn,
			)
			n.recipient_set = [order.player for order in orders if order.coalition == MDCVoteOrder.MDC_OPPOSITIONS[official_line]]


class MDCLineCPUBTask(ResolutionTask):
	"""
	Enforce the effects of the MDC CPUB party line
	"""

	# Resolve after MDCVoteTask
	RESOLUTION_ORDER = 300

	def run(self, game):
		# Because this is run the turn of the vote, we have to ask for the next line, not the current one
		coalition = game.get_mdc_coalition(turn=game.current_turn + 1)

		if coalition != MDCVoteOrder.CPUB:
			return

		win_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn, coalition=MDCVoteOrder.CPUB)
		for o in win_votes:
			for c in o.get_friendly_corporations():
				c.update_assets(1, category=AssetDelta.MDC)

		loss_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn, coalition=MDCVoteOrder.DEVE)
		for o in loss_votes:
			for c in o.get_friendly_corporations():
				c.update_assets(-1, category=AssetDelta.MDC)


class MDCLineDEVETask(ResolutionTask):
	"""
	Enforce the effects of the MDC DEVE party line
	"""

	# Resolve after MDCVoteTask
	RESOLUTION_ORDER = 300

	def run(self, game):

		# Because this is ran the turn of the vote, we have to watch out for the next line
		coalition = game.get_mdc_coalition(turn=game.current_turn + 1)

		if coalition != MDCVoteOrder.DEVE:
			return

		win_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn, coalition=MDCVoteOrder.DEVE)
		for o in win_votes:
			for c in o.get_friendly_corporations():
				c.update_assets(1, category=AssetDelta.MDC)

		loss_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn, coalition=MDCVoteOrder.CPUB)
		for o in loss_votes:
			for c in o.get_friendly_corporations():
				c.update_assets(-1, category=AssetDelta.MDC)


tasks = (MDCVoteTask, MDCLineCPUBTask, MDCLineDEVETask)
