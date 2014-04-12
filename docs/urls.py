from django.conf.urls import patterns, url
from docs import views

urlpatterns = patterns('',
	url(r'(?P<page>(\w|/)*)\.md$', views.redirect_md),
	url(r'corporations/(?P<corporation_slug>(\w|/)*)$', views.corporation),
	url(r'(?P<page>(\w|/)*)$', views.index),
)
