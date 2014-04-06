from django.contrib import admin

from engine_modules.corporation.models import Corporation, AssetDelta
from engine_modules.corporation_asset_history.models import AssetHistory


class AssetHistoryInline(admin.TabularInline):
	model = AssetHistory


class CorporationAdmin(admin.ModelAdmin):
	inlines = [AssetHistoryInline]
	list_display = ('name', 'game', 'assets')

	def name(self, instance):
		return instance.base_corporation.name
admin.site.register(Corporation, CorporationAdmin)


class AssetDeltaAdmin(admin.ModelAdmin):
	list_display = ('corporation', 'delta', 'category', 'turn')
admin.site.register(AssetDelta, AssetDeltaAdmin)
