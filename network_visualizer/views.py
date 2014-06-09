from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django import forms
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

class QueryForm(forms.Form):
    query = forms.IntegerField()

def query_author(request):
    response = {}
    if request.method == 'POST':
        print(request.POST)
        response['success'] = True;
        query = QueryForm(request.POST)
        if query.is_valid():
            print("query is valid")
            context = query_list[0](query['query'].value())
            return context
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response['success'] = False
        print(response)
        return HttpResponse(json.dumps(response), content_type="application/json")
        # print(query)
        # if query.is_valid():
            # context = query_list[0](query['query'].value())
            # return context
        # return {'success':false}

def query_paper(request):
    if request.method == 'POST':
        query = QueryForm(request.POST)
        if query.is_valid():
            context = query_list[1](query['query'].value())
            return context
# Create your views here.



