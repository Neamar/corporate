from django.contrib import admin
from messaging.models import Message, Newsfeed


class MessageAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'content')
	list_filter = ('recipient_set__game',)
	ordering = ('author',)
admin.site.register(Message, MessageAdmin)


class NewsfeedAdmin(admin.ModelAdmin):
	list_display = ('category', 'turn', 'path', 'content')
	list_filter = ('game',)
admin.site.register(Newsfeed, NewsfeedAdmin)
