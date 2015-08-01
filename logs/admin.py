from django.contrib import admin
from logs.models import Logs


class LogsAdmin(admin.ModelAdmin):
	list_display = ('event_type', 'delta', 'game', 'data', 'turn')
admin.site.register(Logs, LogsAdmin)
