from engine.models import Order


class BuyInfluenceOrder(Order):
	"""
	Order to increase Player Influence
	"""
	pass


orders = (BuyInfluenceOrder,)
