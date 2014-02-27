# -*- coding: utf-8 -*-
from django.db import models
from django.utils.functional import cached_property

from engine_modules.corporation_run.models import OffensiveRunOrder
from engine.models import Player
from messaging.models import Message

information_messages = {
	'success': {
		'sponsor': u"Votre équipe a réussi à retrouver les rapports de %s",
		'citizens': u"Les informations personnelles de %s ont été dérobées par %s.",
	},
	'fail': {
		'sponsor': u"Votre équipe a échoué et n'a rien trouvé concernant les agissements de %s",
		'citizens': u"Une tentative de vol d'informations personnelles a été effectuée sur %s pour le compte de %s",
	},
}


class InformationOrder(OffensiveRunOrder):
	title = "Lancer une run d'Information"

	TIMING_MALUS_SIMILAR = 'player'
	PROTECTION_TYPE = "datasteal"
	BASE_SUCCESS_PROBABILITY = 60

	target = models.ForeignKey(Player)

	@cached_property
	def target_corporation(self):
		return self.target.citizenship.corporation

	def resolve_success(self, detected):
		target_orders = self.target.message_set.filter(flag=Message.RESOLUTION).order_by('-turn')

		self.player.add_message(
			title="Run d'information sur %s" % (self.target),
			content="\n".join(["## Tour %s\n\n%s" % (o.turn, o.content) for o in target_orders]),
			author=None,
			flag=Message.PRIVATE_MESSAGE,
		)

		category = u"Run d'Information"
		content = information_messages['success']['sponsor'] % (self.target.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = information_messages['success']['citizens'] % (self.target.name, self.player.name)
			self.notify_citizens(content)

	def resolve_fail(self, detected):
		# Send a note to the one who ordered the DataSteal
		category = u"Run d'Information"
		content = information_messages['fail']['sponsor'] % (self.target.name)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = information_messages['fail']['citizens'] % (self.target.name, self.player.name)
			self.notify_citizens(content)

	def description(self):
		return "Lancer une run d'information sur %s" % self.target

orders = (InformationOrder, )
