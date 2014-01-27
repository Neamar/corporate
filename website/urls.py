from django.conf.urls import patterns, url
from website.views import index

urlpatterns = patterns('',
	url(r'^$', index),
	url(r'^login/$', 'django.contrib.auth.views.login'),
)
