# -*- coding: utf-8 -*-
from engine.tasks import OrderResolutionTask
from engine_modules.player_run.models import InformationOrder


class InformationRunTask(OrderResolutionTask):
	"""
	First log all the InformationOrders in Logs. So informationOrders launched by other users are an available information
	Then Resolve Information runs at the end
	"""
	RESOLUTION_ORDER = 1200
	ORDER_TYPE = InformationOrder

	def run(self, game):
		orders = self.ORDER_TYPE.objects.filter(player__game=game, turn=game.current_turn)
		for order in orders:
			players = order.player_targets.all()
			corpos = list(order.corporation_targets.all())
			# add event on player
			game.add_event(event_type=game.OPE_INFORMATION, data={"players_list": [p.name for p in players], "corpos_list": [c.base_corporation.name for c in corpos]}, players=[order.player])
			# send the background information on targets players
			for player in players:
				game.add_event(event_type=game.BACKGROUND, data={"background": player.background, "player": player.name}, players=[order.player])

		for order in orders:
			order.resolve_successful()


class InformationPayTask(OrderResolutionTask):
	"""
	As MoneyInformationTask is at RESOLUTION_ORDER 1100 and need both things to be right
	-To be start before InformationRunTask
	-All the payments must be payed before this task
	So we pay information at 1000 and we start it at 1200
	"""
	RESOLUTION_ORDER = 1000
	ORDER_TYPE = InformationOrder

	def run(self, game):
		orders = self.ORDER_TYPE.objects.filter(player__game=game, turn=game.current_turn)
		for order in orders:
			order.pay_cost()


tasks = (InformationRunTask, InformationPayTask)
