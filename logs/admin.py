from django.contrib import admin
from logs.models import Log, ConcernedPlayer


class ConcernedPlayerInline(admin.TabularInline):
	model = ConcernedPlayer


class LogAdmin(admin.ModelAdmin):
	list_display = ('event_type', 'delta', 'game', 'data', 'turn')
	inlines = [ConcernedPlayerInline]

admin.site.register(Log, LogAdmin)
