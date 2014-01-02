# -*- coding: utf-8 -*-
from engine.tasks import OrderResolutionTask
from engine_modules.citizenship.models import CitizenShipOrder


class CitizenshipTask(OrderResolutionTask):
	"""
	Update player citizenship
	"""
	RESOLUTION_ORDER = 900
	ORDER_TYPE = CitizenShipOrder
	
	def run(self):
		"""
		Send a note for final message
		"""
		title=u"Citoyenneté"
		content=u"Vous êtes désormais citoyen de la mégacorporation %s." % self.ORDER_TYPE.corporation
		self.player.add_note(title=title, content=content)

tasks = (CitizenshipTask,)
