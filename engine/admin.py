from django.contrib import admin
from engine.models import Game, Player, Order


class PlayerInline(admin.TabularInline):
	model = Player
	exclude = ('secrets',)
	extra = 1


class GameAdmin(admin.ModelAdmin):
	inlines = [PlayerInline]
	list_display = ('city', 'current_turn', 'total_turn')
	actions = ("resolve_current_turn",)

	def resolve_current_turn(self, request, queryset):
		for game in queryset:
			game.resolve_current_turn()
	resolve_current_turn.short_description = "Resolve current turn now"

admin.site.register(Game, GameAdmin)


class PlayerAdmin(admin.ModelAdmin):
	list_display = ('name', 'user', 'game')
	list_filter = ('game',)
	ordering = ('name',)
admin.site.register(Player, PlayerAdmin)


class OrderAdmin(admin.ModelAdmin):
	list_display = ('type', 'player', 'cost', 'turn')
	readonly_fields = ('turn',)
	list_filter = ('player__game',)
	ordering = ('player',)
admin.site.register(Order, OrderAdmin)
