# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.forms import widgets

from engine_modules.run.models import RunOrder
from engine_modules.corporation.models import Corporation
from engine_modules.market.models import CorporationMarket
from engine.models import Game

from collections import OrderedDict
import string
import random


class DropdownWidget(widgets.Select):
	"""
	Widget to be used in Run classes so that we have a list of lists by Corporation then Market
	every time we have to chose a CorporationMarket.
	"""

	def __init__(self, *args, **kwargs):
		container_id = "None"
		if 'container_id' in kwargs:
			container_id = kwargs['container_id']
			del(kwargs['container_id'])

		super(DropdownWidget, self).__init__(*args, **kwargs)
		self.data = args[0]
		self.container_id = container_id

	def render(self, name, value, attrs=None, choices=()):

		# print 'name: {0}'.format(name)
		# print 'value: {0}'.format(value)
		# print 'attrs: {0}'.format(attrs)
		# print 'choices: {0}'.format(choices)

		tmpid = ''
		for i in range(20):
			tmpid += random.choice(string.lowercase)
		print tmpid

		html = '<div class=hidden id=' + tmpid + '>\n' + super(DropdownWidget, self).render(name, value, attrs, choices=choices) + '\n</div>'
		html += '<div class="dropdown" id=dd_' + tmpid + '>\n<ul>\n    <li>\n Corporations\n' + ' ' * 8 + '<ul>\n'
		for key in self.data.keys():
			html += ' ' * 12 + '<li>\n' + ' ' * 16 + '{0}\n'.format(str(key)) + ' ' * 16 + '<ul>\n'
#			html += ' ' * 16 + '<select id="{0}" name="{1}" onchange="{1}">\n'.format(attrs['id'], name, '')
			for value in self.data[key]:
				try:
					html += u' ' * 20 + u'<li onclick="{0}">\n'.format('dropdown_select(\'' + tmpid + '\', ' + str(value.id) + ');') + u' ' * 24 + u'{0}\n'.format(value.market.name) + u' ' * 20 + u'</li>\n'
#				html += ' ' * 20 + '<option value="{0}">{1}</option>\n'.format(value.id, str(value))
				except Exception,e:
					print str(e)
			html += ' ' * 16 + '</ul>\n' + ' ' * 12 + '</li>\n'
		html += '        </ul>\n    </li>\n</ul>\n</div>'
		# print "in render: {0}".format(html)
		return html

	def value_from_datadict(self, data, files, name):
		# print 'data: {0}'.format(data)
		# print 'files: {0}'.format(files)
		# print 'name; {0}'.format(name)

		for i in dict(data.iterlists())['target_corporation_market']:
			if i != u'':
				return string.atoi(i)


class CorporationRunOrder(RunOrder):
	"""
	Model for offensive corporation runs.
	"""

	target_corporation_market = models.ForeignKey(CorporationMarket, related_name="scoundrels")

	def get_success_probability(self):
		"""
		Compute success probability, eventually modified by protection runs
		"""
		base_value = super(CorporationRunOrder, self).get_success_probability()

		protection = self.target_corporation_market.protectors.filter(
			turn=self.turn
		)
		if protection.exists():
			return min(base_value, ProtectionOrder.MAX_PERCENTS)
		return base_value

	@property
	def target_corporation(self):
		"""
		Helper function to directly retrieve the corporation from its market
		"""
		return self.target_corporation_market.corporation

	def get_form(self, data=None):
		form = super(CorporationRunOrder, self).get_form(data)
		# We get all the corporationMarket of uncrashed corporations
		form.fields['target_corporation_market'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game, corporation__crash_turn__isnull=True, turn=self.player.game.current_turn)
		corporation_markets = {}
		for cm in form.fields['target_corporation_market'].queryset:
			if cm.corporation not in corporation_markets.keys():
				corporation_markets[cm.corporation] = []
			corporation_markets[cm.corporation].append(cm)

		print 'type: %s' % self.type
		choices = [(i.id, str(i)) for i in form.fields['target_corporation_market'].queryset]
		form.fields['target_corporation_market'].widget = DropdownWidget(corporation_markets, container_id="lol", choices=choices)

		return form


class CorporationRunOrderWithStealer(CorporationRunOrder):
	"""
	Offensive run with a stealer (e.g. DataStealOrder / ExtractionOrder)
	"""
	stealer_corporation = models.ForeignKey(Corporation, related_name="+")

	@property
	def stealer_corporation_market(self):
		"""
		Helper function to directly retrieve the market for the stealer
		"""
		return self.stealer_corporation.corporationmarket_set.get(market=self.target_corporation_market.market_id, turn=self.player.game.current_turn)

	def get_form(self, data=None):
		form = super(CorporationRunOrderWithStealer, self).get_form(data)
		form.fields['stealer_corporation'].widget = forms.Select(attrs={'onchange': 'get_targets(this);'})
		form.fields['stealer_corporation'].queryset = self.player.game.corporation_set.all()
		# We have to reverse the fields to go from more specific to less specific
		# This ensures that stealer_corporation will be above target_corporation_market
		items = form.fields.items()
		items.reverse()
		form.fields = OrderedDict(items)
		return form


class DataStealOrder(CorporationRunOrderWithStealer):
	"""
	Order for DataSteal runs
	"""
	ORDER = 500

	title = "Lancer une opération de Datasteal"

	def resolve_successful(self):
		self.stealer_corporation.update_assets(+1, corporation_market=self.stealer_corporation_market)

		# create a game_event on the stealer
		self.player.game.add_event(event_type=Game.OPE_DATASTEAL_UP, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, delta=1, corporation=self.stealer_corporation, corporation_market=self.stealer_corporation_market, players=[self.player])
		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_DATASTEAL_DOWN, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def resolve_failure(self):
		# create a game_event on the stealer
		self.player.game.add_event(event_type=Game.OPE_DATASTEAL_FAIL_UP, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.stealer_corporation, corporation_market=self.stealer_corporation_market, players=[self.player])
		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_DATASTEAL_FAIL_DOWN, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def description(self):
		return u"Envoyer une équipe voler des données de %s (%s) pour le compte de %s" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.stealer_corporation.base_corporation.name)


class ExtractionOrder(CorporationRunOrderWithStealer):
	"""
	Order for Extraction runs
	"""
	ORDER = 700
	title = "Lancer une opération d'Extraction"

	def resolve_successful(self):
		self.target_corporation.update_assets(-1, corporation_market=self.target_corporation_market)
		self.stealer_corporation.update_assets(1, corporation_market=self.stealer_corporation_market)

		# create a game_event on the stealer
		self.player.game.add_event(event_type=Game.OPE_EXTRACTION_UP, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, delta=1, corporation=self.stealer_corporation, corporation_market=self.stealer_corporation_market, players=[self.player])
		# create a game_event on the target
		self.player.game.add_event(event_type=Game.OPE_EXTRACTION_DOWN, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, delta=-1, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def resolve_failure(self):
		# create a game_event on the stealer
		self.player.game.add_event(event_type=Game.OPE_EXTRACTION_FAIL_UP, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.stealer_corporation, corporation_market=self.stealer_corporation_market, players=[self.player])
		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_EXTRACTION_FAIL_DOWN, data={"player": self.player.name, "market": self.stealer_corporation_market.market.name, "corporation_target": self.target_corporation.base_corporation.name, "corporation_stealer": self.stealer_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def description(self):
		return u"Réaliser une extraction de %s (%s) vers %s" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name, self.stealer_corporation.base_corporation.name)


class SabotageOrder(CorporationRunOrder):
	"""
	Order for Sabotage runs
	"""
	ORDER = 600
	title = "Lancer une opération de Sabotage"

	def resolve_successful(self):
		self.target_corporation.update_assets(-2, corporation_market=self.target_corporation_market)

		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_SABOTAGE, delta=-2, data={"player": self.player.name, "market": self.target_corporation_market.market.name, "corporation": self.target_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def resolve_failure(self):
		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_SABOTAGE_FAIL, data={"player": self.player.name, "market": self.target_corporation_market.market.name, "corporation": self.target_corporation.base_corporation.name, "chances": self.get_raw_probability()}, corporation=self.target_corporation, corporation_market=self.target_corporation_market, players=[self.player])

	def description(self):
		return u"Envoyer une équipe saper les opérations et les résultats de %s (%s)" % (self.target_corporation.base_corporation.name, self.target_corporation_market.market.name)

	def get_form(self, data=None):
		form = super(SabotageOrder, self).get_form(data)
		# we can't make a sabotage on a negative or null corporationMarket
		form.fields['target_corporation_market'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game, corporation__crash_turn__isnull=True, turn=self.player.game.current_turn, value__gt=0)

		return form


class ProtectionOrder(RunOrder):
	"""
	Order for Protection runs
	"""
	ORDER = 850
	title = "Lancer une opération de Protection"
	MAX_PERCENTS = 40

	protected_corporation_market = models.ForeignKey(CorporationMarket, related_name="protectors")

	@property
	def protected_corporation(self):
		"""
		Helper function to directly retrieve the corporation from its market
		"""
		return self.protected_corporation_market.corporation

	def resolve(self):
		self.player.money -= self.get_cost()
		self.player.save()

		# create a game event on the target
		self.player.game.add_event(event_type=Game.OPE_PROTECTION, data={"player": self.player.name, "market": self.protected_corporation_market.market.name, "corporation": self.protected_corporation.base_corporation.name}, corporation=self.protected_corporation, corporation_market=self.protected_corporation_market, players=[self.player])

	def description(self):
		return u"Envoyer une équipe protéger %s" % (self.protected_corporation.base_corporation.name)

	def get_form(self, data=None):
		form = super(ProtectionOrder, self).get_form(data)
		form.fields['protected_corporation_market'].queryset = CorporationMarket.objects.filter(corporation__game=self.player.game, turn=self.player.game.current_turn)

		return form


orders = (DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder)
