from django.conf.urls import patterns, url
from website import views

urlpatterns = patterns('',
	url(r'^$', views.index),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^game/(?P<game_id>[0-9]+)/orders$', views.orders),
)
