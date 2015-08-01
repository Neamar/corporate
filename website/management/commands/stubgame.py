from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from engine.models import Game, Player


class Command(BaseCommand):
	help = 'Create a stub game for testing'

	def create_user(self, password, **kwargs):
		User = get_user_model()
		user, created = User.objects.get_or_create(**kwargs)
		user.set_password(password)
		user.save()
		return user

	def create_player(self, game, **kwargs):
		p = Player(**kwargs)
		game.player_set.add(p)
		return p

	def handle(self, *args, **options):
		# Create admin user
		self.stdout.write("Creating admin...")
		self.create_user(password="admin", username="admin", is_staff=True, is_superuser=True)

		# Create other users
		self.stdout.write("Creating users...")
		user1 = self.create_user(password="user", username="player1")
		user2 = self.create_user(password="user", username="player2")
		user3 = self.create_user(password="user", username="player3")
		user4 = self.create_user(password="user", username="player4")

		# Create game
		self.stdout.write("Creating stub game...")
		g = Game.objects.create(city="Stub")
		p1 = self.create_player(game=g, user=user1, name="player1", background="Player 1 background")
		g.player_set.add(p1)
		p2 = Player(user=user2, name="player1", background="Player 2 background")
		g.player_set.add(p2)
		p3 = Player(user=user3, name="player1", background="Player 3 background")
		g.player_set.add(p3)
		p4 = Player(user=user4, name="player1", background="Player 4 background")
		g.player_set.add(p4)
