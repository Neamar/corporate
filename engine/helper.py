# -*- coding: utf-8 -*-
from engine.models import Message

def build_message_from_notes(message_type, note_type, title, recipient_set, opening='', ending='', **kwargs):
	"""
	Envoie un message en récupérant toutes les notes d'un types triées par titre de message.
	une note de titre T1 contenu C1, une T1 C2 et une T2 C3, on récupère ce message :

	## T1
	* C1
	* C2

	## T2
	* C3
	"""

	messages = Message.objects.filter(flag=note_type, **kwargs).order_by('title')
	resolution_message=opening
	past_title=""
	for message in messages:
		current_title=message.title
		if current_title==past_title:
			resolution_message += u"* %s\n" % message.content
		else:
			resolution_message += u"\n## %s\n* %s\n" % (message.title, message.content) #Change Bold title if this isn't right
		past_title=current_title
	resolution_message+=ending
	m=Message.objects.create(
			title=title,
			content=resolution_message,
			author=None,
			flag=message_type)
	m.save()
	m.recipient_set=recipient_set
	return m