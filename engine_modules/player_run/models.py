# -*- coding: utf-8 -*-
from django.db import models
from django.utils.functional import cached_property

from engine_modules.corporation_run.models import OffensiveRunOrder
from engine.models import Player
from messaging.models import Message
from website.widgets import PlainTextField

information_messages = {
	'success': {
		'sponsor': u"Votre équipe a *réussi* une run d'**information** sur %s",
		'citizens': u"Une run d'**information**, commanditée par %s, a *réussi* sur %s avec %s%% chances de réussite",
	},
	'fail': {
		'sponsor': u"Votre équipe a *échoué* sa run d'*information** sur %s",
		'citizens': u"Une run d'**information**, commanditée par %s, a *échoué* sur %s avec %s%% chances de réussite",
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
		messages = "\n".join(["### Tour %s\n\n%s" % (o.turn, o.content.replace('# ', '## ')) for o in target_orders])

		self.player.add_message(
			title="Run d'information sur %s" % (self.target),
			content="## Secrets du joueur\n%s\n\n## Feuilles d'Ordres\n%s" % (secrets, messages),
			author=None,
			flag=Message.PRIVATE_MESSAGE,
		)

		category = u"Run d'Information"
		content = information_messages['success']['sponsor'] % (self.target)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = information_messages['success']['citizens'] % (self.player, self.target, self.get_raw_probability())
			self.notify_citizens(content)

	def resolve_fail(self, detected):
		# Send a note to the one who ordered the DataSteal
		category = u"Run d'Information"
		content = information_messages['fail']['sponsor'] % (self.target)
		self.player.add_note(category=category, content=content)

		if detected:
			# Send a note to citizens
			content = information_messages['fail']['citizens'] % (self.player, self.target, self.get_raw_probability())
			self.notify_citizens(content)

	def get_form(self, datas=None):
		form = super(InformationOrder, self).get_form(datas)
		form.fields['base_percents'] = PlainTextField(initial="%s%%" % self.BASE_SUCCESS_PROBABILITY)

		return form

	def description(self):
		return "Lancer une run d'information sur %s" % self.target

orders = (InformationOrder, )
