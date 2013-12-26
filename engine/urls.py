from django.conf.urls import patterns, url
from engine.views import index

urlpatterns = patterns('',
	url(r'(?P<game_id>[0-9]+)$', index),
	url(r'^(?P<game_id>[0-9]+)/players$', players),
)
