from parse import *
from summarize import *
from categorize.get_keywords import *

class FeedContent:
  def __init__(self,sum_len=2):
    self.summary_len = sum_len
    self.summarizer = FrequencySummarizer()
    self.categorizer = CategorizeNewsArticle()
    # search terms
    #self.getSearchResults()
    self.getContent()
    pass

  # return list of urls to parse
  def getSearchResults(self): pass

  def getContent(self):
    # loop through articles to parse
    articleContent = {}
    url=u'http://www.nydailynews.com/news/politics/rudy-giuliani-people-living-shelters-aren-home-article-1.2357767/'
    parser = ParseArticle(url)
    articleContent["article"] = parser.getArticleData()
    articleText = articleContent["article"]["text"]

    articleContent["summary"] = self.summarizer.summarize(articleText,self.summary_len)

    articleContent["keywords"] = self.categorizer.run(articleText)
    return articleContent