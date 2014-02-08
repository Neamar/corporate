from collections import Counter
from engine.tasks import ResolutionTask
from engine_modules.mdc.models import MDCVoteSession, MDCVoteOrder


class MDCVoteTask(ResolutionTask):
	"""
	Choose the MDC party line
	"""
	resolution_order = 100
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
tasks = (MDCVoteTask, )
