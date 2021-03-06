# -*- coding: utf-8 -*-
from collections import Counter
from engine.tasks import ResolutionTask
from engine_modules.detroit_inc.models import DIncVoteSession, DIncVoteOrder
from engine.models import Game

import string


class DIncVoteTask(ResolutionTask):
	"""
	Choose the Detroit, Inc. party line, and save it in a DIncVoteSession
	"""
	RESOLUTION_ORDER = 100
	ORDER_TYPE = DIncVoteOrder

	def run(self, game):
		orders = DIncVoteOrder.objects.filter(player__game=game, turn=game.current_turn)

		self.create_logs(orders)
		official_line = self.get_official_line(orders)
		explaination_text = self.get_explaination_text(orders)

		s = DIncVoteSession(
			coalition=official_line,
			game=game,
			turn=game.current_turn + 1,
			explaination_text=explaination_text
		)
		s.save()

		if official_line is not None:
			# We create a game_event for each winner
			winners = [order.player for order in orders if order.coalition == official_line]
			event_type = None
			# the case of CPUB is handled in DIncLineCPUBTask to access the random corporationmarket
			if official_line == DIncVoteOrder.RSEC:
				event_type = Game.EFFECT_SECURITY_UP
			elif official_line == DIncVoteOrder.CONS:
				event_type = Game.EFFECT_CONSOLIDATION_UP
			if event_type is not None:
				game.add_event(event_type=event_type, data=None, players=winners)

			# We create a game_event for each loser
			losers = [order.player for order in orders if order.coalition == DIncVoteOrder.DINC_OPPOSITIONS[official_line]]
			event_type = None
			if official_line == DIncVoteOrder.RSEC:
				event_type = Game.EFFECT_SECURITY_DOWN
			elif official_line == DIncVoteOrder.CONS:
				event_type = Game.EFFECT_CONSOLIDATION_DOWN
			if event_type is not None:
				game.add_event(event_type=event_type, data=None, players=losers)

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

	def get_explaination_text(self, orders):
		"""
		Write a peace of text to explain what just happens in detroit inc
		"""
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

			siders = " ".join(["<li>%s" % s for s in siders])

			content = u"<strong>%s</strong> a reçu <strong>%s</strong> voix : <ul>%s</ul>" % (coalition, count, siders)

			coalition_breakdown.append(content)

		if not coalition_breakdown:
			return u"Personne n'a choisi de coalition ce tour-ci"

		return string.join(coalition_breakdown, '')

	def create_logs(self, orders):
		"""
		Create logs for votes
		"""
		for order in orders:
			if order.coalition == DIncVoteOrder.CPUB:
				event_type = Game.VOTE_CONTRAT
			elif order.coalition == DIncVoteOrder.RSEC:
				event_type = Game.VOTE_SECURITY
			elif order.coalition == DIncVoteOrder.CONS:
				event_type = Game.VOTE_CONSOLIDATION
			if event_type is not None:
				order.player.game.add_event(event_type=event_type, data={'weight': order.get_weight()}, players=[order.player])


class DIncLineCPUBTask(ResolutionTask):
	"""
	Enforce the effects of the Detroit, Inc. CPUB party line
	"""

	# Resolve after DIncVoteTask
	RESOLUTION_ORDER = 500

	def run(self, game):
		# Because this is run the turn of the vote, we have to ask for the next line, not the current one
		coalition = game.get_dinc_coalition(turn=game.current_turn + 1)

		if coalition != DIncVoteOrder.CPUB:
			return

		win_votes = DIncVoteOrder.objects.filter(player__game=game, turn=game.current_turn, coalition=DIncVoteOrder.CPUB)
		for o in win_votes:
			for c in o.get_friendly_corporations():
				# increase a market by 1 asset at random
				corporation_market = c.get_random_corporation_market()
				c.update_assets(1, corporation_market=corporation_market)
				game.add_event(event_type=Game.EFFECT_CONTRAT_UP, data={"market": corporation_market.market.name}, delta=1, corporation=c, corporation_market=corporation_market)

		loss_votes = DIncVoteOrder.objects.filter(player__game=game, turn=game.current_turn, coalition=DIncVoteOrder.RSEC)
		for o in loss_votes:
			for c in o.get_friendly_corporations():
				# decrease a market by 1 asset at random
				corporation_market = c.get_random_corporation_market()
				c.update_assets(-1, corporation_market=c.get_random_corporation_market())
				game.add_event(event_type=Game.EFFECT_CONTRAT_DOWN, data={"market": corporation_market.market.name}, delta=-1, corporation=c, corporation_market=corporation_market)

tasks = (DIncVoteTask, DIncLineCPUBTask)
