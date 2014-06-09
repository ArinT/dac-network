from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# ... the rest of your URLconf goes here ...
urlpatterns = patterns('',
    url(r'^$', 'network_visualizer.views.index', name='index'),
    url(r'^proto1', 'network_visualizer.views.proto1', name='proto1'),
    url(r'^proto2', 'network_visualizer.views.proto2', name='proto2'),
    url(r'^proto3', 'network_visualizer.views.proto3', name='proto3'),
    url(r'^citation', 'network_visualizer.views.citation', name='citation'),
    url(r'^query_author', 'network_visualizer.views.query_author', name='query_author'),
    url(r'^query_paper', 'network_visualizer.views.query_paper', name='query_paper'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()