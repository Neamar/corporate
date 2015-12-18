from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from engine.models import Game, Player


class Command(BaseCommand):
	help = 'Create a stub game for testing'

	def create_user(self, username, **kwargs):
		User = get_user_model()
		user, created = User.objects.get_or_create(username=username, **kwargs)
		user.set_password(username)
		user.save()
		return user

	def create_player(self, game, **kwargs):
		p = Player(**kwargs)
		game.player_set.add(p)
		return p

	def handle(self, *args, **options):
		# Create admin user
		self.stdout.write("Creating admin...")
		admin = self.create_user(username="admin", is_staff=True, is_superuser=True)

		# Create other users
		self.stdout.write("Creating users...")
		user1 = self.create_user(username="player1")
		user2 = self.create_user(username="player2")
		user3 = self.create_user(username="player3")
		user4 = self.create_user(username="player4")

		# Create game
		self.stdout.write("Creating stub game...")
		self.g = Game.objects.create(city="Stub")
		self.p1 = self.create_player(game=self.g, user=user1, name="player1", background="Player 1 background")
		self.p2 = self.create_player(game=self.g, user=user2, name="player2", background="Player 2 background")
		self.p3 = self.create_player(game=self.g, user=user3, name="player3", background="Player 3 background")
		self.p4 = self.create_player(game=self.g, user=user4, name="player4", background="Player 4 background")
		self.p5 = self.create_player(game=self.g, user=admin, name="player5-admin", background="Player 5 background")

		self.stdout.write("Created game #%s, connect with username `player1` and password `player1`" % self.g.pk)
