# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.forms import ModelForm, Textarea


class MessageManager(models.Manager):
	def get_discussion(self, receiver, sender):
		"""
		return all the messages and update read messages status
		"""
		messages = Message.objects.filter(Q(receiver=receiver, sender=sender) | Q(receiver=sender, sender=receiver)).order_by('creation')
		for message in messages:
			if message.receiver == receiver and message.read is False:
				message.read = True
				message.save()
		return messages


class Message(models.Model):
	"""
	Messages from a player to an other player
	"""
	objects = MessageManager()

	sender = models.ForeignKey('engine.Player', related_name='sender')
	receiver = models.ForeignKey('engine.Player', related_name='receiver')
	content = models.CharField(max_length=300)
	read = models.BooleanField(default=False)
	creation = models.DateTimeField(auto_now_add=True)


class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ['content']
		widgets = {
			'content': Textarea(attrs={'cols': 35, 'rows': 4}),
		}

	def __init__(self, *args, **kwargs):
		super(MessageForm, self).__init__(*args, **kwargs)
		self.fields['content'].label = ""
