from django.db import models

from engine.models import Order, Player


class WiretransferOrder(Order):
	"""
	Send money to another player.
	Immediate effect.
	"""

	recipient = models.ForeignKey(Player)
	value = models.PositiveIntegerField(help_text="En milliers de nuyens")

	def save(self, *args):
		# Override save: apply immediately and return
		pass
