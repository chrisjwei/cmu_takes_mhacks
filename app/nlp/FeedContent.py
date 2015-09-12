import json, requests
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
    ## loop through params,  and make separate calls, update same obj.
    self.encodeParams() 
    # search terms
    self.getSearchResults()
    self.getContent()
    pass

  def encodeParams(self): 
    # pass look keywords
    self.encodedParams = "homeless"
    return 

  # return list of urls to parse
  def getSearchResults(self): 
    pass
    full_url = self.url + "&q=%s" % self.encodedParams
    response = requests.get(full_url)
    data = json.loads(response.text)
    self.rawData = data["responseData"]["results"]
    
  def processContent(self):
    for article in self.rawData:
      articleContent = {}
      url = article[u'unescapedUrl']
      parser = ParseArticle(url)
      articleContent["article"] = parser.getArticleData()
      try: articleContent["article"]["language"] = article["language"]
      except: articleContent["article"]["language"] = None
      try: articleContent["article"]["location"] = article["location"]
      except: articleContent["article"]["location"] = None
      try: articleContent["article"]["image"] = article["image"]
      except: articleContent["article"]["image"] = None
      articleText = articleContent["article"]["text"]

      articleContent["summary"] = self.summarizer.summarize(articleText,self.summary_len)

      articleContent["keywords"] = self.categorizer.run(articleText)
      self.articles.append(articleContent)
    return

  def getContent(self):
    return {"articles": self.articles}