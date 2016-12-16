from django.contrib import admin
from logs.models import Log, ConcernedPlayer


class ConcernedPlayerInline(admin.TabularInline):
	model = ConcernedPlayer


class LogAdmin(admin.ModelAdmin):
	list_display = ('event_type', 'delta', 'game', 'data', 'turn', 'corporation', 'display')

	def display(self, log):
		try:
			return log.get_display('corporation')
		except:
			return log.get_display('player')

	inlines = [ConcernedPlayerInline]

admin.site.register(Log, LogAdmin)
