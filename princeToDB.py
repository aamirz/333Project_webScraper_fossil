"""
postScrapedArticle.py
Author: Aamir Zainulabadeen

POSTS an article to our database.
"""
import scrapePrince as sp
import requests as req

# scrape an article with url and post it
def postOne(pageUrl):
    js = sp.jsonify_page(url = pageUrl)

    # POST REQUEST
    url = "something"
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=js, headers=headers)
    
