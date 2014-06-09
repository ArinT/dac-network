from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django import forms
import json
from django.shortcuts import render_to_response, redirect
from network_visualizer.query_database import *
import json

query_list = [get_author_info,get_paper_info]
def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
def proto1(request):
    template = loader.get_template('proto1.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
def proto2(request):
    template = loader.get_template('proto2.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
def proto3(request):
    template = loader.get_template('proto3.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
def citation(request):
    template = loader.get_template('citations.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

class QueryAuthorForm(forms.Form):
    author_id = forms.IntegerField()
class QueryPaperForm(forms.Form):
    paper_id = forms.IntegerField()

def query_author(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = QueryAuthorForm(data)
        if query.is_valid():
            context = query_list[0](query['author_id'].value())
            return context

def query_paper(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = QueryPaperForm(data)
        if query.is_valid():
            context = query_list[1](query['paper_id'].value())
            return context# Create your views here.



