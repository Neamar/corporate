from django.conf.urls import patterns, url
from docs import views

urlpatterns = patterns('',
	url(r'(?P<page>\w+)$', views.index),
)
