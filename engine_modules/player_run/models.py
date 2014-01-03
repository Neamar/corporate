from django.db import models
from engine_modules.run.models import RunOrder
from engine.models import Player, Message


class InformationRunOrder(RunOrder):
	target = models.ForeingKey(Player)

	def resolve_successful(self):
		target_orders = Message.objects.filter(recipient_set=self.target, flag=Message.ORDER).order_by('pk')[-1]
		self.player.add_message(
			title="Run d'information sur %s, tour " % (self.target, self.game.current_turn),
			content=target_orders.content,
			author=None,
			flag=Message.RUN
		)

