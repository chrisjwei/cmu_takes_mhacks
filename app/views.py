"""
Definition of views.
"""
import sys
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

sys.path.insert(0, 'app/nlp/')
import getFeedContent

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    charities = []
    with open('app/data/charities.txt','r') as f:
    	for line in f:
    		charities.append(line.rstrip());
    print charities
    return render(
        request,
        'app/index.html')
    

def newsfeed(request):
    """Renders the newsfeed page."""
    assert isinstance(request, HttpRequest)
    artcles = getFeedContent()
    return render(
        request,
        'app/newsfeed.html')

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

def getFeedContent():
  sampleObj = {'articles':[
              {
                'meta_data':{
                  'matched_keywords':['keyword11','keyword12']
                  
                },
                'article':{
                  'title':'title1',
                  'url':'url1',
                  'author':['author11','author12'],
                  'publish_date':'date1',
                  'location':'geography1',
                  'text':'text1'
                },
                'summary':'summary of article1',
                'keywords':['keyword11','keyword12']
              },
              {
                'meta_data':{
                  'matched_keywords':['keyword21','keyword22']
                  
                },
                'article':{
                  'title':'title2',
                  'url':'url2',
                  'author':['author21','author22'],
                  'publish_date':'date2',
                  'location':'geography2',
                  'text':'text2'
                },
                'summary':'summary of article2',
                'keywords':['keyword21','keyword22']
              },
              {
                'meta_data':{
                  'matched_keywords':['keyword31','keyword32']
                  
                },
                'article':{
                  'title':'title3',
                  'url':'url3',
                  'author':['author31','author32'],
                  'publish_date':'date3',
                  'location':'geography3',
                  'text':'text3'
                },
                'summary':'summary of article3',
                'keywords':['keyword31','keyword32']
              }]
          }
  return sampleObj