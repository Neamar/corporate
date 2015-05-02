# -*- coding: utf-8 -*-
from collections import Counter
from engine.tasks import ResolutionTask
from engine_modules.corporation.models import AssetDelta
from engine_modules.detroit_inc.models import DIncVoteSession, DIncVoteOrder
from messaging.models import Newsfeed, Note
from engine.models import Game


class DIncVoteTask(ResolutionTask):
	"""
	Choose the Detroit, Inc. party line, and save it in a DIncVoteSession
	"""
	RESOLUTION_ORDER = 100
	ORDER_TYPE = DIncVoteOrder

	def run(self, game):
		orders = DIncVoteOrder.objects.filter(player__game=game, turn=game.current_turn)

		self.send_resolution_message(orders)
		official_line = self.get_official_line(orders)

		s = DIncVoteSession(
			coalition=official_line,
			game=game,
			turn=game.current_turn + 1
		)
		s.save()

		self.send_newsfeed(orders, s)

		if official_line is not None:
			# Message all player who voted for this line
			n = Note.objects.create(
				category=Note.DINC,
				content="Detroit, Inc. a suivi votre coalition",
				turn=game.current_turn,
			)
			n.recipient_set = [order.player for order in orders if order.coalition == official_line]

			n = Note.objects.create(
				category=Note.DINC,
				content=u"Detroit, Inc. a rejoint la coalition opposée: %s" % s.get_coalition_display(),
				turn=game.current_turn,
			)
			n.recipient_set = [order.player for order in orders if order.coalition == DIncVoteOrder.DINC_OPPOSITIONS[official_line]]

	def get_official_line(self, orders):
		"""
		With specified orders, retrieve official line.
		"""

		votes_count = {}
		for t in DIncVoteOrder.DINC_OPPOSITIONS.values():
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
			order.player.add_note(category=Note.DINC, content="Vous avez rejoint la coalition *%s*." % order.get_coalition_display())
			if order.get_coalition_display() == 'Contrats publics':
				event_type = Game.VOTE_CONTRAT
			elif order.get_coalition_display() == u'Réforme de la sécurité':
				event_type = Game.VOTE_SECURITY
			elif order.get_coalition_display() == 'Consolidation':
				event_type = Game.VOTE_CONSOLIDATION
			order.player.game.create_game_event(event_type=event_type, data='', players=[order.player])


	def send_newsfeed(self, orders, dinc_vote_session):
		"""
		Build newsfeed message. Contains official line, and breakdown for each coalition.
		"""

		if dinc_vote_session.coalition is not None:
			dinc_vote_session.game.add_newsfeed(category=Newsfeed.DINC_REPORT, content=u"La coalition *%s* a été votée par Detroit Inc." % dinc_vote_session.get_coalition_display())

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
			dinc_vote_session.game.add_newsfeed(category=Newsfeed.DINC_REPORT, content=u"Répartition des coalitions :\n\n  * %s" % ("\n  * ".join(coalition_breakdown)))


class DIncLineCPUBTask(ResolutionTask):
	"""
	Enforce the effects of the Detroit, Inc. CPUB party line
	"""

	# Resolve after DIncVoteTask
	RESOLUTION_ORDER = 300

	def run(self, game):
		# Because this is run the turn of the vote, we have to ask for the next line, not the current one
		coalition = game.get_dinc_coalition(turn=game.current_turn + 1)

		if coalition != DIncVoteOrder.CPUB:
			return

		win_votes = DIncVoteOrder.objects.filter(player__game=game, turn=game.current_turn, coalition=DIncVoteOrder.CPUB)
		for o in win_votes:
			for c in o.get_friendly_corporations():
				# increase a market by 1 asset at random
				corporationmarket=c.random_corporation_market
				c.update_assets(1, category=AssetDelta.DINC, corporationmarket=corporationmarket)
				game.create_game_event(event_type=Game.EFFECT_CONTRAT_UP, data='',  delta=1 , corporation=c , corporationmarket=corporationmarket)


		loss_votes = DIncVoteOrder.objects.filter(player__game=game, turn=game.current_turn, coalition=DIncVoteOrder.RSEC)
		for o in loss_votes:
			for c in o.get_friendly_corporations():
				# decrease a market by 1 asset at random
				corporationmarket=c.random_corporation_market
				c.update_assets(-1, category=AssetDelta.DINC, corporationmarket=c.random_corporation_market)
				game.create_game_event(event_type=Game.EFFECT_CONTRAT_DOWN, data='',  delta=-1 , corporation=c , corporationmarket=corporationmarket)

tasks = (DIncVoteTask, DIncLineCPUBTask)
