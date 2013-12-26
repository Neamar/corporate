from django.contrib import admin
from engine.models import Game, Message, Player, Order

class GameAdmin(admin.ModelAdmin):
	list_display = ('current_turn', 'total_turn')

class PlayerAdmin(admin.ModelAdmin):
	list_display = ('user', 'name', 'game')

class MessageAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'public', 'player', 'public')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('player', 'game', 'turn')