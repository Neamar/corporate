from django.conf.urls import patterns, url
from website.views import index, data, orders

# Index views
urlpatterns = patterns('',
	url(r'^$', index.index),
	url(r'^login$', 'django.contrib.auth.views.login'),
	url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
	url(r'^signup$', 'website.views.index.signup'),
)

# Data views
urlpatterns += patterns('',
	url(r'^game/(?P<game_id>[0-9]+)/wallstreet$', data.wallstreet),
	url(r'^game/(?P<game_id>[0-9]+)/wallstreet/(?P<turn>[0-9]+)$', data.wallstreet),
	url(r'^game/(?P<game_id>[0-9]+)/corporations/(?P<corporation_slug>[a-z0-9-]+)$', data.corporation),
	url(r'^game/(?P<game_id>[0-9]+)/corporations/(?P<corporation_slug>[a-z0-9-]+)/(?P<turn>[0-9]+)$', data.corporation),
	url(r'^game/(?P<game_id>[0-9]+)/player/(?P<player_id>[0-9]+)$', data.player),
	url(r'^game/(?P<game_id>[0-9]+)/player/(?P<player_id>[0-9]+)/(?P<turn>[0-9]+)$', data.player),
	url(r'^game/(?P<game_id>[0-9]+)/shares$', data.shares),
	url(r'^game/(?P<game_id>[0-9]+)/shares/(?P<turn>[0-9]+)$', data.shares),
)

# Orders views
urlpatterns += patterns('',
	url(r'^game/(?P<game_id>[0-9]+)/orders$', orders.orders),
	url(r'^game/(?P<game_id>[0-9]+)/orders/new/(?P<order_type>\w+)$', orders.add_order),
	url(r'^game/(?P<game_id>[0-9]+)/orders/delete/(?P<order_id>\w+)$', orders.delete_order),
)
