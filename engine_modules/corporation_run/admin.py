from django.contrib import admin

from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder

class DataStealOrderAdmin(admin.ModelAdmin):
	list_display = ('pk', 'has_succeeded', 'target_corporation', 'stealer_corporation')
admin.site.register(DataStealOrder, DataStealOrderAdmin)


class ProtectionOrderAdmin(admin.ModelAdmin):
	list_display = ('protected_corporation', 'done')
admin.site.register(ProtectionOrder, ProtectionOrderAdmin)


class SabotageOrderAdmin(admin.ModelAdmin):
	list_display = ('pk', 'target_corporation')
admin.site.register(SabotageOrder, SabotageOrderAdmin)
