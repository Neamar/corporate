from django.contrib import admin

from engine_modules.corporation.models import Corporation
from engine_modules.corporation_asset_history.models import AssetHistory


class AssetHistoryInline(admin.TabularInline):
	model = AssetHistory


class CorporationAdmin(admin.ModelAdmin):
	inlines = [AssetHistoryInline]
	list_display = ('name', 'game', 'assets')
	list_filter = ('game',)

	def name(self, instance):
		return instance.base_corporation.name
admin.site.register(Corporation, CorporationAdmin)
