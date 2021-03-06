from django.contrib import admin
from engine_modules.market.models import Market, CorporationMarket


class MarketAdmin(admin.ModelAdmin):
	list_display = ('game', 'name')

admin.site.register(Market, MarketAdmin)


class CorporationMarketAdmin(admin.ModelAdmin):
	list_display = ('game', 'corporation', 'market', 'turn', 'value')
	list_filter = ('corporation__game', 'corporation', 'market', 'turn', )

	def game(self, instance):
		return instance.corporation.game

admin.site.register(CorporationMarket, CorporationMarketAdmin)
