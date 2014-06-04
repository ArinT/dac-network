from django.contrib import admin

from network_visualizer.models import Papers
from network_visualizer.models import Authors
from network_visualizer.models import Cocredits
admin.site.register(Papers)
admin.site.register(Authors)
admin.site.register(Cocredits)