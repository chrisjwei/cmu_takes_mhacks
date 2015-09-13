"""
Definition of views.
"""
import sys
import json
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

sys.path.insert(0, 'app/nlp/')
from FeedContent import *

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    charities = []
    
    return render(
        request,
        'app/index.html', context)
    

def newsfeed(request):
    """Renders the newsfeed page."""
    assert isinstance(request, HttpRequest)
    charity = request.GET.get('charity', False)
    if (charity):
    	request.session['charity'] = charity
    else:
    	return redirect('/');


    articles = FeedContent(charity)
    articles.processContent()
    content = articles.getContent()
    return render(
        request,
        'app/newsfeed.html', content)

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/about.html');
