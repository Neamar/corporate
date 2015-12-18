from django.contrib import admin
from engine_modules.citizenship.models import Citizenship, CitizenshipOrder


class CitizenshipAdmin(admin.ModelAdmin):
	list_display = ('player', 'corporation', 'turn', 'game')
	list_filter = ('corporation__game',)

	def game(self, instance):
		return instance.corporation.game
admin.site.register(Citizenship, CitizenshipAdmin)
admin.site.register(CitizenshipOrder)
