from django.contrib import admin

from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder, SabotageOrder, ExtractionOrder


class ProtectionOrderAdmin(admin.ModelAdmin):
	list_display = ('pk', 'protected_corporation')
admin.site.register(ProtectionOrder, ProtectionOrderAdmin)


class DataStealOrderAdmin(admin.ModelAdmin):
	list_display = ('pk', 'target_corporation', 'stealer_corporation')
admin.site.register(DataStealOrder, DataStealOrderAdmin)


class SabotageOrderAdmin(admin.ModelAdmin):
	list_display = ('pk', 'target_corporation')
admin.site.register(SabotageOrder, SabotageOrderAdmin)


class ExtractionOrderAdmin(admin.ModelAdmin):
	list_display = ('pk', 'target_corporation', 'kidnapper_corporation')
admin.site.register(ExtractionOrder, ExtractionOrderAdmin)
