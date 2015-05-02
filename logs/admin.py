from django.contrib import admin
from logs.models import Logs


class LogsAdmin(admin.ModelAdmin):
	list_display = ('category', 'delta', 'game', 'content', 'turn')
admin.site.register(Logs, LogsAdmin)
