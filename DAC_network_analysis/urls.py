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
    url(r'^chrono', 'network_visualizer.views.chrono', name='chrono'),
    url(r'^freqplot', 'network_visualizer.views.freqplot', name='freqplot'),
    url(r'^topicbubble', 'network_visualizer.views.topicbubble', name='topicbubble'),
    url(r'^phrasetimeline', 'network_visualizer.views.topicbubble', name='phrasetimeline'),
    url(r'^query_author', 'network_visualizer.views.query_author', name='query_author'),
    url(r'^query_paper', 'network_visualizer.views.query_paper', name='query_paper'),
    url(r'^send_email', 'network_visualizer.views.send_email', name='send_email'),
    url(r'^get_clusters', 'network_visualizer.views.get_clusters', name='get_clusters'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()