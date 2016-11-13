from django.contrib import admin
from engine_modules.player_points.models import PlayerPoints


class PlayerPointsAdmin(admin.ModelAdmin):
	list_display = ('player', 'total_points', 'citizenship_points', 'background_points', 'dinc_points')
	list_filter = ('player',)


admin.site.register(PlayerPoints, PlayerPointsAdmin)
