from django.contrib import admin

from engine_modules.detroit_inc.models import DIncVoteSession, DIncVoteOrder


class DIncVoteSessionAdmin(admin.ModelAdmin):
	list_display = ('turn', 'coalition', 'game')
	readonly_fields = ('game', 'turn')
admin.site.register(DIncVoteSession, DIncVoteSessionAdmin)


class DIncVoteOrderAdmin(admin.ModelAdmin):
	list_display = ('turn', 'player', 'coalition', 'get_weight')
admin.site.register(DIncVoteOrder, DIncVoteOrderAdmin)
