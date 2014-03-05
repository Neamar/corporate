# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.utils.functional import cached_property

from engine_modules.corporation_run.models import OffensiveRunOrder
from engine.models import Player
from messaging.models import Message
from website.widgets import PlainTextWidget

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
	"""
	Order for Information runs
	"""
	title = "Lancer une run d'Information"

	TIMING_MALUS_SIMILAR = 'player'
	PROTECTION_TYPE = "datasteal"
	BASE_SUCCESS_PROBABILITY = 60

	target = models.ForeignKey(Player)

	@cached_property
	def target_corporation(self):
		return self.target.citizenship.corporation

	def resolve_success(self, detected):
		secrets = self.target.secrets

		target_orders = self.target.message_set.filter(flag=Message.RESOLUTION).order_by('-turn')
		messages = "\n".join(["### Tour %s\n\n%s" % (o.turn, o.content) for o in target_orders])

		self.player.add_message(
			title="Run d'information sur %s" % (self.target),
			content="## Secrets du joueur\n%s\n\n## Feuilles d'Ordres\n%s" % (secrets, messages),
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

	def get_form(self, datas=None):
		form = super(InformationOrder, self).get_form(datas)
		form.fields['base_percents'] = forms.CharField(initial="%s%%" % self.BASE_SUCCESS_PROBABILITY, widget=PlainTextWidget)

		return form
	def description(self):
		return "Lancer une run d'information sur %s" % self.target

orders = (InformationOrder, )
