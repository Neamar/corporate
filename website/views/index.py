from __future__ import absolute_import

from website.decorators import render
from website.models import User


@render('index.html')
def index(request):
	"""
	Welcome to the Corporate Game!
	"""

	players = []
	if type(request.user) == User:
		players = request.user.player_set.all().select_related('game')

	return {
		"players": players
	}
