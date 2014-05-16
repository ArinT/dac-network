from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# ... the rest of your URLconf goes here ...
urlpatterns = patterns('',
    url(r'^$', 'network_visualizer.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()