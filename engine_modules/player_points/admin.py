from django.contrib import admin

from engine_modules.player_points.models import PlayerPoints


class CorporationAdmin(admin.ModelAdmin):
	inlines = [PlayerPoints]
	list_display = ('player', 'total_points', 'citizenship_points', 'background_points', 'dinc_points')
	list_filter = ('player',)
