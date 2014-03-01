from django.contrib import admin

from engine_modules.mdc.models import MDCVoteSession, MDCVoteOrder


class MDCVoteSessionAdmin(admin.ModelAdmin):
	list_display = ('party_line', 'game', 'turn')
	readonly_fields = ('game', 'turn')
admin.site.register(MDCVoteSession, MDCVoteSessionAdmin)


class MDCVoteOrderAdmin(admin.ModelAdmin):
	list_display = ('party_line', 'get_weight')
admin.site.register(MDCVoteOrder, MDCVoteOrderAdmin)
