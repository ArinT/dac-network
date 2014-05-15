from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect
def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
# Create your views here.
