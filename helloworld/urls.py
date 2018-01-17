# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include
from django.conf import settings
from django.views.generic.base import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from fb_scraper import views as newsletter_views

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^helloworld/', include('helloworld.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Hello, world!
    (r'^fetch_data/', 'helloworld.views.fetch_data'),
    (r'^signup/', newsletter_views.signupform),
    (r'', TemplateView.as_view(template_name='index.html'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

