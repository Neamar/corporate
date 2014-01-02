from engine.tasks import OrderResolutionTask
from engine_modules.influence.models import BuyInfluenceOrder


class BuyInfluenceTask(OrderResolutionTask):
	"""
	Buy new Influence level
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = BuyInfluenceOrder

	def run(self):
		"""
		Send a note for final message
		"""
		title=u"Influence"
		content=u"Votre Influence dans le milieu corporatiste monte à %s." % self.ORDER_TYPE.player.influence.level
		self.player.add_note(title=title, content=content)


tasks = (BuyInfluenceTask,)
