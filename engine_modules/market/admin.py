from django.contrib import admin
from engine_modules.market.models import Market, CorporationMarket


class MarketAdmin(admin.ModelAdmin):
	list_display = ('game', 'name')

admin.site.register(Market, MarketAdmin)


class CorporationMarketAdmin(admin.ModelAdmin):
	list_display = ('corporation', 'market', 'turn', 'value')

admin.site.register(CorporationMarket, CorporationMarketAdmin)
