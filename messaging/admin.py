from django.contrib import admin
from messaging.models import Message, Note


class MessageAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'content')
	ordering=('author',)
admin.site.register(Message, MessageAdmin)


class NoteAdmin(admin.ModelAdmin):
	list_display = ('category', 'content')
admin.site.register(Note, NoteAdmin)
