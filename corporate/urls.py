from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'game/', include('engine.urls')),
	url(r'', include('website.urls')),
	)
