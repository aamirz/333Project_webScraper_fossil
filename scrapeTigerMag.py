"""
scrapeTigerMag.py

Author: Aamir Zainulabadeen 

Scrape the contents of the Tiger magazine @ http://www.tigermag.com/

"""

import scrapeBase as sb

# fulfill the scrapeBase API 
# topicId is a list of topics 
def jsonify_page(urls, topicId, switch="JSON"):
    return 0


# fulfill the scrapeBase API
# get all urls for a current date
def getAllUrls(date, topics):
    return 0


# for an article's soup, get the title
def getTitle(soup):
    dirtyTitle = soup.select(".hentry-meta h1")
    caught = sb.listCatch()
