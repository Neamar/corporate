from django.contrib import admin

from engine_modules.corporation.models import Corporation


class CorporationAdmin(admin.ModelAdmin):
	list_display = ('name', 'game', 'assets')

	def name(self, instance):
		return instance.base_corporation.name
admin.site.register(Corporation, CorporationAdmin)
