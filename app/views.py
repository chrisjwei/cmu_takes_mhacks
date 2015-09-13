"""
Definition of views.
"""
import sys
import json
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.template.loader import render_to_string
from datetime import datetime
from django.http import HttpResponse
from pymongo import *

sys.path.insert(0, 'app/nlp/')
from FeedContent import *

mongo = MongoClient('localhost', 27017)
db = mongo.cache

def parseCharityList():
	with open('app/data/charities.json') as data_file:    
		charities_obj = json.load(data_file)
	return charities_obj

def getContentFromQuery(query):
	articles = FeedContent(query)
	articles.processContent()
	content = articles.getContent()
	queryDoc = {'query' : query}
	document = dict(content.items() + queryDoc.items())
	db.myCache.update_one(queryDoc, {'$set' : {'articles' : content['articles']}}, True)
	return content

def home(request):
	"""Renders the home page."""
	assert isinstance(request, HttpRequest)
	charities = []
	for key in parseCharityList():
		charities.append(key);
	context = {'charityList': charities}
	return render(
	    request,
	    'app/index.html', context)
def fake(request):
	print 'dummy'
def filter(request):
	filter_type = request.GET.get('type_of_filter', False)
	if (filter_type == 'incidents'):
		charity = request.session['charity']
		keywords = parseCharityList()[charity]
		masterList = []
		for keyword in keywords:
			keywordArticles = getContentFromQuery(keyword)
			masterList += keywordArticles['articles']
		content = {'articles' : masterList}
		print content
		html = render_to_string('app/newsfeed.html', content)
		return HttpResponse(html)

def newsfeed(request):
	"""Renders the newsfeed page."""
	assert isinstance(request, HttpRequest)
	charity = request.GET.get('charity', False)
	if (charity):
		request.session['charity'] = charity
	else:
		print "no GET argument"
		return redirect('/');

	doc = db.myCache.find_one({'query' : charity})
	if(doc):
		content = doc
	else:	
		content = getContentFromQuery(charity)

	return render(
	    request,
	    'app/newsfeed.html', content)

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/about.html');
