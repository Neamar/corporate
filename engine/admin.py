from django.contrib import admin
from engine.models import Game, Message, Player, Order

class GameAdmin(admin.ModelAdmin):
	list_display = ('current_turn', 'total_turn')
admin.site.register(Game, GameAdmin)

class PlayerAdmin(admin.ModelAdmin):
	list_display = ('user', 'name', 'game')
	ordering=('name',)
admin.site.register(Player, PlayerAdmin)

class MessageAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'public', 'content')
	ordering=('author',)
admin.site.register(Message, MessageAdmin)

class OrderAdmin(admin.ModelAdmin):
	list_display = ('player', 'turn')
	ordering=('player',)
admin.site.register(Order, OrderAdmin)