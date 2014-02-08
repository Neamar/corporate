from django.db import models


class Newsfeed(models.Model):
	pass

class Message(models.Model):
	ORDER = 'ORD'
	PRIVATE_MESSAGE = 'PM'
	RESOLUTION = 'RE'

	MESSAGE_CHOICES = (
		(ORDER, 'Order'),
		(PRIVATE_MESSAGE, 'Private Message'),
		(RESOLUTION, 'Resolution'),
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
	def build_message_from_notes(message_type, notes, title, turn, opening="", ending=""):
		"""
		Generate from QuerySet notes a message, aggregating by notes titles. Will also remove notes from DB.
		With notes category T1 and content C1, note T1 C2 and T2 C3 final message will be (markdown):

		## T1
		* C1
		* C2

		## T2
		* C3
		"""

		notes = notes.order_by('category')
		resolution_message = opening + "\n"
		last_title = ""

		for note in notes:
			if note.category != last_title:
				resolution_message += u"\n## %s\n" % note.category
			resolution_message += u"* %s\n" % note.content
			last_title = note.category

		resolution_message += "\n" + ending + "\n"

		m = Message.objects.create(
			title=title,
			content=resolution_message,
			author=None,
			flag=message_type,
			turn=turn
		)

		return m


class Note(models.Model):
	category = models.CharField(max_length=256)
	content = models.TextField(blank=True)
	recipient_set = models.ManyToManyField('engine.Player')
	turn = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return "%s (%s)" % (self.category, self.turn)


# Import signals
from messaging.signals import *
