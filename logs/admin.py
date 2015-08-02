from django.contrib import admin
from logs.models import Logs, ConcernedPlayers


class ConcernedPlayersInline(admin.TabularInline):
	model = ConcernedPlayers


class LogsAdmin(admin.ModelAdmin):
	list_display = ('event_type', 'delta', 'game', 'data', 'turn')
	inlines = [ConcernedPlayersInline]

admin.site.register(Logs, LogsAdmin)
