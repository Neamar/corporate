from __future__ import absolute_import

from website.decorators import render


@render('index.html')
def index(request):
	"""
	Welcome to the Corporate Game!
	"""

	players = []

	if request.user.is_authenticated():
		players = request.user.player_set.all().select_related('game')

	return {
		"players": players
	}
