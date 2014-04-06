from django.contrib import admin
from engine_modules.corporation_asset_history.models import AssetHistory


class AssetHistoryAdmin(admin.ModelAdmin):
	list_display = ('corporation', 'turn', 'assets')
	list_filter = ('corporation__game',)
admin.site.register(AssetHistory, AssetHistoryAdmin)
