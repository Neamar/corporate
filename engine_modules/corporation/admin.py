from django.contrib import admin

from engine_modules.corporation.models import BaseCorporation, Corporation


class BaseCorporationAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
admin.site.register(BaseCorporation, BaseCorporationAdmin)


class CorporationAdmin(admin.ModelAdmin):
	list_display = ('name', 'game', 'assets')

	def name(self, instance):
		return instance.base_corporation.name
admin.site.register(Corporation, CorporationAdmin)
