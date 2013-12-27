from django.conf.urls import patterns, url
from engine import views

urlpatterns = patterns('',
	url(r'(?P<game_id>[0-9]+)$', views.index),
	url(r'^(?P<game_id>[0-9]+)/players$', views.players),
)
