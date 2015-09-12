import json, requests, urllib
from parse import *
from summarize import *
from categorize.get_keywords import *

class FeedContent:
  def __init__(self,keywords,sum_len=2):
    self.articles = []
    self.rawData = []
    self.url = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&rsz=8"
    self.summary_len = sum_len
    self.summarizer = FrequencySummarizer()
    self.categorizer = CategorizeNewsArticle()

    self.keywords = keywords
    ## loop through params,  and make separate calls, update same obj.
    self.encodeParams() 
    # search terms
    self.getSearchResults()
    self.getContent()
    pass

  def encodeParams(self):
    # self.encodedParams = urllib.request.quote(self.keywords)
    keywords = {'q':self.keywords}
    self.encodedParams = urllib.urlencode(keywords)
    return 

  # return list of urls to parse
  def getSearchResults(self): 
    full_url = self.url + "&%s" % self.encodedParams
    response = requests.get(full_url)
    data = json.loads(response.text)
    self.rawData = data["responseData"]["results"]
    
  def processContent(self):
    for article in self.rawData:
      articleContent = {}
      url = article[u'unescapedUrl']
      if "forbes" not in url:
        parser = ParseArticle(url)
        articleContent["article"] = parser.getArticleData()
        try: articleContent["article"]["language"] = article["language"]
        except: articleContent["article"]["language"] = None
        try: articleContent["article"]["location"] = article["location"]
        except: articleContent["article"]["location"] = None
        try: articleContent["article"]["image"] = article["image"]
        except: articleContent["article"]["image"] = None
        articleText = articleContent["article"]["text"]

        # minor preprocessing to clean up around encodings, meta data, and miscellaneous titles

        articleText = articleText.encode('ascii', 'ignore')
        articleText = articleText.replace('\n',' ')
        articleText = re.sub('\{[^>]+\}',"",articleText)
        articleText = re.sub('\{\*[^>]+\*\}',"",articleText)
        articleText = articleText.replace('&amp;','&')
        articleText = articleText.replace('&quot;','\"')
        articleText = articleText.replace('&apos;','\'')
        articleText = articleText.replace('&gt;','>')
        articleText = articleText.replace('&lt;','<')
        
        spamWords = {'Share Pin It ', 'More Galleries ', 'ADVERTISEMENT '}
        # phrases like posted on removed elsewhere
        for word in spamWords:
          articleText = articleText.replace(word,'')
        
        if len(articleText.split()) > 100:
          articleContent["summary"] = self.summarizer.summarize(articleText,self.summary_len)
          articleContent["keywords"] = [] 
          try:
            keywords = self.categorizer.run(articleText)
            for kw in keywords:
              articleContent["keywords"].append(kw.replace('\n',' '))
          except:
              pass
          self.articles.append(articleContent)
    return

  def getContent(self):
    return {"articles": self.articles}