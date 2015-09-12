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