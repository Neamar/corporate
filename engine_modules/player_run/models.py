from django.db import models
from engine_modules.run.models import RunOrder
from engine.models import Player
from messaging.models import Message


class InformationRunOrder(RunOrder):
	target = models.ForeignKey(Player)

	def resolve_successful(self):
		target_orders = self.target.message_set.filter(flag=Message.ORDER, turn=self.player.game.current_turn)[0]

		self.player.add_message(
			title="Run d'information sur %s, tour %s" % (self.target, self.player.game.current_turn),
			content=target_orders.content,
			author=None,
			flag=Message.PRIVATE_MESSAGE,
		)
