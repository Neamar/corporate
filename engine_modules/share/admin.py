from django.contrib import admin

from engine_modules.share.models import Share
from engine_modules.share.orders import BuyShareOrder


class ShareAdmin(admin.ModelAdmin):
	list_display = ('corporation', 'player', 'turn')
	readonly_fields = ('turn',)
admin.site.register(Share, ShareAdmin)


class BuyShareAdmin(admin.ModelAdmin):
	list_display = ('player', 'corporation', 'turn')
admin.site.register(BuyShareOrder, BuyShareAdmin)
