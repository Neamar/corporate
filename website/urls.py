from django.conf.urls import patterns, url
from website import views

urlpatterns = patterns('',
	url(r'^$', views.index),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^game/(?P<game_id>[0-9]+)/orders$', views.orders),
	url(r'^game/(?P<game_id>[0-9]+)/orders/post/(?P<order_type>\w+)$', views.add_order),
	url(r'^game/(?P<game_id>[0-9]+)/wallstreet$', views.wallstreet),
	url(r'^game/(?P<game_id>[0-9]+)/corporations$', views.corporations),
	url(r'^game/(?P<game_id>[0-9]+)/players$', views.players),
)
