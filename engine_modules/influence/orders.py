from engine.models import Order


class BuyInfluenceOrder(Order):
	"""
	Order to increase Player Influence
	"""
	def save(self):
		self.type = "BuyInfluenceOrder"
		super(BuyInfluenceOrder, self).save()


__orders__ = (BuyInfluenceOrder,)
