from django.contrib import admin

from network_visualizer.models import Papers
from network_visualizer.models import Authors
from network_visualizer.models import Cocredits
from network_visualizer.models import Citations
from network_visualizer.models import Works
from network_visualizer.models import Keywords
from network_visualizer.models import Keywordtopaper
from network_visualizer.models import Topfives

admin.site.register(Papers)
admin.site.register(Authors)
admin.site.register(Cocredits)
admin.site.register(Citations)
admin.site.register(Works)
admin.site.register(Keywords)
admin.site.register(Keywordtopaper)
admin.site.register(Topfives)