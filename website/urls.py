from django.conf.urls import patterns, url
from website.views import index, datas, orders

# Index views
urlpatterns = patterns('',
	url(r'^$', index.index),
	url(r'^login$', 'django.contrib.auth.views.login'),
	url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
)

# Datas views
urlpatterns += patterns('',
	url(r'^game/(?P<game_id>[0-9]+)/newsfeeds$', datas.newsfeeds),
	url(r'^game/(?P<game_id>[0-9]+)/newsfeeds/(?P<turn>[0-9]+)$', datas.newsfeeds),
	url(r'^game/(?P<game_id>[0-9]+)/comlink$', datas.comlink),
	url(r'^game/(?P<game_id>[0-9]+)/comlink/(?P<message_id>[0-9]+)$', datas.message),
	url(r'^game/(?P<game_id>[0-9]+)/wallstreet$', datas.wallstreet),
	url(r'^game/(?P<game_id>[0-9]+)/wallstreet/(?P<turn>[0-9]+)$', datas.wallstreet),
	url(r'^game/(?P<game_id>[0-9]+)/corporations$', datas.corporations),
	url(r'^game/(?P<game_id>[0-9]+)/corporations/(?P<corporation_slug>[a-z-]+)$', datas.corporation),
	url(r'^game/(?P<game_id>[0-9]+)/players$', datas.players),
	url(r'^game/(?P<game_id>[0-9]+)/players/(?P<player_id>[0-9]+)$', datas.player),
	url(r'^game/(?P<game_id>[0-9]+)/shares$', datas.shares),
	url(r'^game/(?P<game_id>[0-9]+)/shares/(?P<turn>[0-9]+)$', datas.shares),
)

# Orders views
urlpatterns += patterns('',
	url(r'^game/(?P<game_id>[0-9]+)/orders$', orders.orders),
	url(r'^game/(?P<game_id>[0-9]+)/orders/new/(?P<order_type>\w+)$', orders.add_order),
	url(r'^game/(?P<game_id>[0-9]+)/orders/delete/(?P<order_id>\w+)$', orders.delete_order),
)
