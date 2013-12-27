from engine.models import Order


class BuyInfluenceOrder(Order):
	"""
	Order to increase Player Influence
	"""

	BASE_COST = 50

	def get_cost(self):
		return BuyInfluenceOrder.BASE_COST * (self.player.influence.level + 1)

	def resolve(self):
		# Pay.
		self.player.money -= self.get_cost()
		self.player.save()

		# Increase player influence by one
		self.player.influence.level += 1
		self.player.influence.save()


orders = (BuyInfluenceOrder,)
