from engine.tasks import ResolutionTask
from engine_modules.citizenship.orders import CitizenShipOrder

class CitizenshipTask(ResolutionTask):
	"""
	Add a citizenship to a player
	"""
	priority = 90

	def run(self, game):
		"""
		Retrieve all BuyInfluenceOrder and resolve them
		"""
		citizen_ship_orders = CitizenShipOrder.objects.filter(player__game=game, turn=game.current_turn)
		for citizen_ship_order in citizen_ship_orders:
			citizen_ship_orders.resolve()


tasks = (CitizenshipTask,)
