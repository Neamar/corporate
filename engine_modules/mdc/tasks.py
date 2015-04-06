# -*- coding: utf-8 -*-
import random
from collections import Counter
from engine.tasks import ResolutionTask
from engine_modules.corporation.models import AssetDelta
from engine_modules.mdc.models import MDCVoteSession, MDCVoteOrder
from engine_modules.market.models import CorporationMarket
from messaging.models import Newsfeed, Note


class MDCVoteTask(ResolutionTask):
	"""
	Choose the MDC party line, and save it in an MDCVoteSession
	"""
	RESOLUTION_ORDER = 100
	ORDER_TYPE = MDCVoteOrder

	def run(self, game):
		orders = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn)

		self.send_resolution_message(orders)
		official_line = self.get_official_line(orders)

		s = MDCVoteSession(
			coalition=official_line,
			game=game,
			turn=game.current_turn + 1
		)
		s.save()

		self.send_newsfeed(orders, s)

		if official_line is not None:
			# Message all player who voted for this line
			n = Note.objects.create(
				category=Note.MDC,
				content="Detroit Inc. a suivi votre coalition",
				turn=game.current_turn,
			)
			n.recipient_set = [order.player for order in orders if order.coalition == official_line]

			n = Note.objects.create(
				category=Note.MDC,
				content=u"Detroit Inc. a rejoint la coalition opposée: %s" % s.get_coalition_display(),
				turn=game.current_turn,
			)
			n.recipient_set = [order.player for order in orders if order.coalition == MDCVoteOrder.MDC_OPPOSITIONS[official_line]]

	def get_official_line(self, orders):
		"""
		With specified orders, retrieve official line.
		"""

		votes_count = {}
		for t in MDCVoteOrder.MDC_OPPOSITIONS.values():
			votes_count[t] = 0

		for order in orders:
			votes_count[order.coalition] += order.get_weight()

		top_line = Counter(votes_count).most_common(2)
		# Default to None
		official_line = None
		try:
			if top_line[0][1] != top_line[1][1]:
				official_line = top_line[0][0]
		except IndexError:
			# Only one line voted for
			if len(top_line) != 0:
				official_line = top_line[0][0]
		return official_line

	def send_resolution_message(self, orders):
		"""
		Send a note to each player, to remember his choice.
		"""
		for order in orders:
			order.player.add_note(category=Note.MDC, content="Vous avez rejoint la coalition *%s*." % order.get_coalition_display())

	def send_newsfeed(self, orders, mdc_vote_session):
		"""
		Build newsfeed message. Contains official line, and breakdown for each coalition.
		"""

		if mdc_vote_session.coalition is not None:
			mdc_vote_session.game.add_newsfeed(category=Newsfeed.MDC_REPORT, content=u"La coalition *%s* a été votée par Detroit Inc." % mdc_vote_session.get_coalition_display())

		votes_details = {}

		# Build global dict
		coalition_breakdown = []
		for order in orders:
			if(order.coalition not in votes_details):
				votes_details[order.coalition] = {
					"display": order.get_coalition_display(),
					"members": [],
					"count": 0
				}
			votes_details[order.coalition]["members"].append({
				'player':
				order.player,
				'corporations': order.get_friendly_corporations(),
			})
			votes_details[order.coalition]["count"] += order.get_weight()

		for vote in votes_details.values():
			coalition = vote["display"]
			count = vote["count"]

			siders = []
			for member in vote["members"]:
				member_string = unicode(member['player'])
				if len(member['corporations']) > 0:
					member_string += " (%s)" % (", ".join(unicode(c.base_corporation.name) for c in member['corporations']))
				siders.append(member_string)

			siders = ", ".join(siders)

			content = u"La coalition *%s* a reçu %s voix : %s" % (coalition, count, siders)

			coalition_breakdown.append(content)

		if len(coalition_breakdown) > 0:
			mdc_vote_session.game.add_newsfeed(category=Newsfeed.MDC_REPORT, content=u"Répartition des coalitions :\n\n  * %s" % ("\n  * ".join(coalition_breakdown)))


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
				# increase a market by 1 asset at random
				markets = [cm.market for cm in CorporationMarket.objects.filter(corporation=c)]
				c.update_assets(1, category=AssetDelta.MDC, market=random.choice(markets))

		loss_votes = MDCVoteOrder.objects.filter(player__game=game, turn=game.current_turn, coalition=MDCVoteOrder.RSEC)
		for o in loss_votes:
			for c in o.get_friendly_corporations():
				# decrease a market by 1 asset at random
				markets = [cm.market for cm in CorporationMarket.objects.filter(corporation=c)]
				c.update_assets(-1, category=AssetDelta.MDC, market=random.choice(markets))


tasks = (MDCVoteTask, MDCLineCPUBTask)
