from newspaper import Article

class ParseArticle:
  def __init__(self, url=u'http://www.nydailynews.com/news/politics/rudy-giuliani-people-living-shelters-aren-home-article-1.2357767/'):
    self.url = url

  def getArticleData(self):
    article = Article(self.url)
    article.download()
    article.html
    article.parse()

    articleData = {}
    articleData["url"] = self.url
    articleData["title"] = article.title
    articleData["authors"] = article.authors  # list
    articleData["publish_data"] = article.publish_date  # date obj?
    articleData["text"] = article.text  # unicode

    # article.nlp()
    # article.summary
    # article.keywords
    return articleData

