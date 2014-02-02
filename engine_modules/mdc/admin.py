from django.contrib import admin

from engine_modules.mdc.models import MDCVoteSession, MDCVoteOrder

class MDCVoteSessionAdmin(admin.ModelAdmin):
	list_display = ('current_party_line', 'game', 'turn')
	readonly_fields = ('game', 'turn')
admin.site.register(MDCVoteSession, MDCVoteSessionAdmin)

class MDCVoteOrderAdmin(admin.ModelAdmin):
	list_display = ('weight', 'party_line')
admin.site.register(MDCVoteOrder, MDCVoteOrderAdmin)
