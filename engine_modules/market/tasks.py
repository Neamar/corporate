# -*- coding: utf-8 -*-
from engine.tasks import OrderResolutionTask
from engine_modules.market.models import CorporationMarket

class UpdateBubblesTask(OrderResolutionTask):
	"""
	Remove old bubles from assets, calculate bubbles and addthe new bubbles to assets
	"""
	RESOLUTION_ORDER = 500


	def update_and_save(self, corporation_market, bubble_value):
		if corporation_market.bubble == bubble_value:
			return

		corporation_market.bubble = bubble_value
		corporation_market.save()
		corporation_market.corporation.assets += bubble_value - bubble
		corporation.save()


	def run(self, game):

		#define table for  value
		#read each market (all the lines with a market are grouped)
		corporation_markets = CorporationMarket.objects.filter(game=game).order_by('market','-value')
		for corporation_market in corporation_markets:
			#Define the negative bubble
			if (corporation_market.value == 0):
				corporation_market.bubble = -1
			else:
				if corporation_market.market != actuel_market:
					actuel_market = corporation_market.market
					best_value = corporation_market.value
					best_corporation_market = corporation_market
					test_second = True
				else:
					if test_second == True and best_value > corporation_market.value:
						#There are juste one corporation with the best value in this market
						best_corporation_market.bubble = 1
						corporation_market.bubble = 0
					elif test_second == True:
						#There are several corporations with the best value in this market
						best_corporation_market.bubble = 0
						corporation_market.bubble = 0
					else:
						corporation_market.bubble = 0



class UpdateBubblesTask2(UpdateBubblesTask):
	"""
	Same as UpdateBubblesTask but at another RESOLUTION_ORDER
	"""
	RESOLUTION_ORDER = 625


tasks = (UpdateBubblesTask, UpdateBubblesTask2)
