# -*- coding: utf-8 -*-
from engine.models import Message

def build_message_from_notes(message_type, notes, title, recipient_set, opening='', ending=''):
	"""
	Generate from QuerySet notes a message, aggregating by notes titles.
	With notes title T1 and content C1, note T1 C2 and T2 C3 final message will be (markdown):

	## T1
	* C1
	* C2

	## T2
	* C3
	"""

	notes = notes.order_by('title')
	resolution_message = opening
	last_title = ""

	for note in notes:
		if note.title != last_title:
			resolution_message += u"\n## %s\n" % note.title
		resolution_message += u"* %s\n" % note.content
		last_title = note.title

	resolution_message += ending

	m = Message.objects.create(
		title=title,
		content=resolution_message,
		author=None,
		flag=message_type)
	m.recipient_set = recipient_set

	return m
