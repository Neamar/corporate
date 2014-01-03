# -*- coding: utf-8 -*-
from engine.models import Message

def build_message_from_notes(message_type, note_type, title, recipient_set, opening='', ending=''):
	messages = Message.objects.filter(flag=note_type).order_by('title')
	resolution_message=opening
	past_title=""
	for message in messages:
		current_title=message.title
		if current_title==past_title:
			resolution_message += u"%s\n" % message.content
		else:
			resolution_message += u"\n[b]%s[/b]\n%s\n" % (message.title, message.content) #Change Bold title if this isn't right
		past_title=current_title
	resolution_message+=ending
	m=Message.objects.create(
			title=title,
			content=resolution_message,
			author=None,
			flag=message_type)
	m.save()
	m.recipient_set=recipient_set
	return resolution_message