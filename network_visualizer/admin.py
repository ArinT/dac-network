from django.contrib import admin

from network_visualizer.models import DacPaperTable
from network_visualizer.models import AuthorTable
from network_visualizer.models import AuthorCoauthorTable
admin.site.register(DacPaperTable)
admin.site.register(AuthorTable)
admin.site.register(AuthorCoauthorTable)