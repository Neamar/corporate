from collections import Counter
from engine.tasks import OrderResolutionTask
from engine_modules.mdc.models import MDCVoteSession, MDCVoteOrder, MDC_Party_Lines


class MDCVoteTask(OrderResolutionTask):
	"""
	Choose the MDC party line
	"""
	resolution_order = 100
	ORDER_TYPE = MDCVoteOrder

	def run(self, game):
		r = MDCVoteOrder.build_vote_registry(game)
		
		#super(MDCVoteTask, self).run(game)
		orders = self.ORDER_TYPE.objects.filter(player__game=game, turn=game.current_turn)
		votes = {}
		for l in MDC_Party_Lines.keys():
			votes[l] = 0

                for order in orders:
                        order.resolve(r)
			votes[order.party_line] += order.weight

		top_line = Counter(votes).most_common(2)
		official_line = "aucune"
		try:
			if top_line[0][1] != top_line[1][1]:
				official_line = top_line[0][0]
		except(IndexError):
			if len(top_line) != 0:
				official_line = top_line[0][0]

		s = MDCVoteSession(
			current_party_line=official_line,
			game=game,
			turn=game.current_turn+1
		)
		s.save()
tasks = (MDCVoteTask, )
