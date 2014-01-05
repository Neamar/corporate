from django.contrib import admin
from messaging.models import Message


class MessageAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'content')
	ordering=('author',)
admin.site.register(Message, MessageAdmin)
