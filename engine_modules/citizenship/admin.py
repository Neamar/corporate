from django.contrib import admin

from engine_modules.citizenship.models import Citizenship, CitizenshipOrder


class CitizenshipAdmin(admin.ModelAdmin):
	list_display = ('player', 'corporation', 'turn', 'game')
	list_filter = ('game',)

	def corporation(self, instance):
		return self.corporation.base_corporation.name

	def game(self, instance):
		return self.player.game
admin.site.register(Citizenship, CitizenshipAdmin)
admin.site.register(CitizenshipOrder)
