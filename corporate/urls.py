import re
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.core.exceptions import ImproperlyConfigured


def static(prefix, view=serve, **kwargs):
    # overrise the default static method to allow static service in no DEBUG mode
    if not prefix:
        raise ImproperlyConfigured("Empty static prefix not permitted")
    return [
        url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    ]


urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'docs/', include('docs.urls')),
    url(r'', include('website.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
