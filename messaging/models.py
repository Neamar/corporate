from django.db import models



class Message(models.Model):
	ORDER = 'ORD'
	PRIVATE_MESSAGE = 'PM'
	RESOLUTION = 'RE'
	GLOBAL_RESOLUTION = 'GRE'


	MESSAGE_CHOICES = (
		(ORDER, 'Order'),
		(PRIVATE_MESSAGE, 'Private Message'),
		(RESOLUTION, 'Resolution'),
		(GLOBAL_RESOLUTION, 'Global Resolution'),
	)

	title = models.CharField(max_length=256)
	content = models.TextField(blank=True)
	author = models.ForeignKey('engine.Player', null=True, related_name="+")
	recipient_set = models.ManyToManyField('engine.Player')
	flag = models.CharField(max_length=3, choices=MESSAGE_CHOICES)

	@staticmethod
	def build_message_from_notes(message_type, notes, title, opening="", ending=""):
		"""
		Generate from QuerySet notes a message, aggregating by notes titles. Will also remove notes from DB.
		With notes title T1 and content C1, note T1 C2 and T2 C3 final message will be (markdown):

		## T1
		* C1
		* C2

		## T2
		* C3
		"""

		notes = notes.order_by('title')
		resolution_message = opening + "\n"
		last_title = ""

		for note in notes:
			if note.title != last_title:
				resolution_message += u"\n## %s\n" % note.title
			resolution_message += u"* %s\n" % note.content
			last_title = note.title

		resolution_message += "\n" + ending + "\n"

		m = Message.objects.create(
			title=title,
			content=resolution_message,
			author=None,
			flag=message_type)

		# Remove notes once consumed
		notes.delete()

		return m

class Note(models.Model):
	title = models.CharField(max_length=256)
	content = models.TextField(blank=True)
	public = models.BooleanField(default=False)
	recipient_set = models.ManyToManyField('engine.Player')
	is_global = models.BooleanField()


# Import signals
from messaging.signals import *
