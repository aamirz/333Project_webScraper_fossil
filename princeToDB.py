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
    url = "http://localhost:8080"
    headers = {'content-type': 'application/json'}
    response = req.post(url, data=js, headers=headers)
    


# testing with one page url
def main():
    url = "http://www.dailyprincetonian.com/article/2017/03/park-president-impeached"
    postOne(url)


if __name__=="__main__":
    main()
