from django.conf.urls import patterns, url
from website import views

urlpatterns = patterns('',
	url(r'^$', views.index),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^game/(?P<game_id>[0-9]+)/newsfeeds$', views.newsfeeds),
	url(r'^game/(?P<game_id>[0-9]+)/comlink$', views.comlink),
	url(r'^game/(?P<game_id>[0-9]+)/orders$', views.orders),
	url(r'^game/(?P<game_id>[0-9]+)/orders/new/(?P<order_type>\w+)$', views.add_order),
	url(r'^game/(?P<game_id>[0-9]+)/orders/delete/(?P<order_id>\w+)$', views.delete_order),
	url(r'^game/(?P<game_id>[0-9]+)/wallstreet$', views.wallstreet),
	url(r'^game/(?P<game_id>[0-9]+)/corporations$', views.corporations),
	url(r'^game/(?P<game_id>[0-9]+)/corporations/(?P<corporation_id>[0-9])$', views.corporation),
	url(r'^game/(?P<game_id>[0-9]+)/players$', views.players),
	url(r'^game/(?P<game_id>[0-9]+)/players/(?P<player_id>[0-9])$', views.player),
)
