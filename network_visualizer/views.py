from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect, requires_csrf_token, ensure_csrf_cookie, csrf_exempt

from django import forms
import json
from django.shortcuts import render_to_response, redirect
from network_visualizer.query_database import *
import json
from django.core.mail import EmailMessage
import smtplib

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
def chrono(request):
    template = loader.get_template('chrono.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
def freqplot(request):
    template = loader.get_template('freqplot.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
class QueryAuthorForm(forms.Form):
    author_id = forms.IntegerField()
class QueryPaperForm(forms.Form):
    paper_id = forms.IntegerField()
@csrf_exempt
def query_author(request):
    """Takes a post request from the client whose input is a
    author id. Returns various information on this author"""
    if request.method == 'POST':
        a_id = json.loads(request.body)['author_id']
        # data = json.loads(request.body)
        # query = QueryAuthorForm(data)
        # if query.is_valid():
        #     print "fuck now"
            # context = query_list[0](query['author_id'].value())
        context = query_list[0](a_id)
        return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def query_paper(request):
    """Takes a post request from the client whose input is a
    paper id. Returns various information on this paper"""
    if request.method == 'POST':
        data = json.loads(request.body)
        query = QueryPaperForm(data)
        if query.is_valid():
            context = query_list[1](query['paper_id'].value())
            #print(context)
            return HttpResponse(json.dumps(context), content_type="application/json")
@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        email = EmailMessage('Subject', body['message'], to=['dacnetworkanalysis@gmail.com'])
        email.send()
        return HttpResponse(json.dumps({'success':True}), content_type="application/json")
        
