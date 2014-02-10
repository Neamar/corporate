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
		# Default to "NONE"
		official_line = MDCVoteOrder.NONE
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

class MDCLineCPUBTask(ResolutionTask):
	"""
	Enforce the effects of the MDC CPUB party line
	"""

	# To be debated
	resolution_order = 100

	def run(self, game):

		party_line = game.get_current_mdc_party_line()

		if party_line != MDCVoteOrder.CPUB:
			return

		winning_corporations = []
		win_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn - 1, party_line=MDCVoteOrder.CPUB)
		for o in win_votes:
			winning_corporations += o.get_friendly_corporations()
			
		losing_corporations = []
		loss_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn - 1, party_line=MDCVoteOrder.DEVE)
		for o in loss_votes:
			losing_corporations += o.get_friendly_corporations()

		for winslug in winning_corporations:
			c = game.corporation_set.get(base_corporation_slug=winslug)
			c.assets += 1
			c.save()

		for loseslug in losing_corporations:
			c = game.corporation_set.get(base_corporation_slug=loseslug)
			c.assets -= 1
			c.save()
	
tasks = (MDCVoteTask, MDCLineCPUBTask)
