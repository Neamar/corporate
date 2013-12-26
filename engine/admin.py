from django.contrib import admin
from engine.models import Game, Message, Player, Order


class GameAdmin(admin.ModelAdmin):
	list_display = ('city', 'current_turn', 'total_turn')
	actions = ("resolve_current_turn",)

	def resolve_current_turn(self, request, queryset):
		for game in queryset:
			game.resolve_current_turn()
	resolve_current_turn.short_description = "Resolve current turn now"

admin.site.register(Game, GameAdmin)


class PlayerAdmin(admin.ModelAdmin):
	list_display = ('name', 'user', 'game')
	ordering=('name',)
admin.site.register(Player, PlayerAdmin)


class MessageAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'public', 'content')
	ordering=('author',)
admin.site.register(Message, MessageAdmin)


class OrderAdmin(admin.ModelAdmin):
	list_display = ('type', 'player', 'turn')
	ordering=('player',)
admin.site.register(Order, OrderAdmin)
