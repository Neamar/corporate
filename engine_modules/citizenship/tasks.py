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
		citizen_ship_orders = CitizenShipOrder.objects.get(player__game=game, turn=game.current_turn)
		citizen_ship_orders.resolve()

		



tasks = (CitizenshipTask,)
