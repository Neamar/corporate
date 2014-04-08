# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe
from utils.read_markdown import parse_markdown


class Newsfeed(models.Model):
	MDC_REPORT = 'mdc-report'
	MATRIX_BUZZ = 'matrix-buzz'
	PEOPLE = 'people'
	ECONOMY = 'economy'

	CATEGORY_CHOICES = (
		(MDC_REPORT, 'Bulletin du MDC'),
		(MATRIX_BUZZ, 'Matrix Buzz'),
		(PEOPLE, 'People'),
		(ECONOMY, 'Économie'),
	)

	category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
	content = models.TextField(blank=True)
	turn = models.PositiveSmallIntegerField()
	game = models.ForeignKey('engine.Game')
	path = models.CharField(max_length=250)

	def __unicode__(self):
		return "%s newsfeeds" % self.get_category_display()

	def as_html(self):
		content, _ = parse_markdown(self.content)
		return mark_safe(content)

	@property
	def subcategory(self):
		if self.path is None:
			return ''
		else:
			return self.path.split('/')[0]

	@property
	def state(self):
		if self.path is None:
			return ''
		else:
			return self.path.split('/')[-1]


class Message(models.Model):
	PRIVATE_MESSAGE = 'PM'
	CASH_TRANSFER = 'CT'
	RESOLUTION = 'RE'

	MESSAGE_CHOICES = (
		(PRIVATE_MESSAGE, 'Message privé'),
		(RESOLUTION, 'Résolution'),
		(CASH_TRANSFER, 'Envoi d\'argent'),
	)

	title = models.CharField(max_length=256)
	content = models.TextField(blank=True)
	author = models.ForeignKey('engine.Player', null=True, related_name="+")
	recipient_set = models.ManyToManyField('engine.Player')
	flag = models.CharField(max_length=3, choices=MESSAGE_CHOICES)
	turn = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return "%s (%s-%s)" % (self.title, self.flag, self.turn)

	@staticmethod
	def build_message_from_notes(message_type, notes, title, turn, opening=""):
		"""
		Generate from notes a message, aggregating by notes category (using order defined by Note.NOTE_CHOICES).
		"""

		notes = sorted(notes, key=lambda n: Note.NOTE_CHOICES.index((n.category, n.get_category_display())))

		resolution_message = opening + "\n\n"
		last_title = Note.GLOBAL

		for note in notes:
			if note.category != last_title:
				resolution_message += u"\n### %s\n" % note.get_category_display()
			resolution_message += u"* %s\n" % note.content
			last_title = note.category

		m = Message.objects.create(
			title=title,
			content=resolution_message,
			author=None,
			flag=message_type,
			turn=turn
		)

		return m


class Note(models.Model):
	GLOBAL = 'global'
	RUNS = 'runs'
	MDC = 'mdc'
	SPECULATION = 'speculation'
	DIVIDEND = 'dividend'

	NOTE_CHOICES = (
		(GLOBAL, u'Global'),
		(RUNS, u'Runs'),
		(MDC, u'MDC'),
		(SPECULATION, u'Spéculations'),
		(DIVIDEND, u'Dividendes'),
	)

	category = models.CharField(max_length=15, choices=NOTE_CHOICES, default=GLOBAL)
	content = models.TextField(blank=True)
	recipient_set = models.ManyToManyField('engine.Player')
	turn = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return "%s (%s)" % (self.category, self.turn)


# Import signals
from messaging.signals import *
