from django.conf.urls import patterns, url
from website.views import index

urlpatterns = patterns('',
	(r'^favicon.ico$', 'django.views.static.serve', {'document_root': '/path/to/favicon'}),
	url(r'^$', index),
	url(r'^login/$', 'django.contrib.auth.views.login'),
)
