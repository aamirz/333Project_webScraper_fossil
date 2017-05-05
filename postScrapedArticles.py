"""
postScrapedArticles.py
Author: Aamir Zainulabadeen

POSTS articles to our database.
"""
import sys
import scrapePrince as sp
import requests as req
import json
from requests.auth import HTTPBasicAuth

authentication = HTTPBasicAuth('aamirz', 'aamirziscool')

# get all of today's articles that have already been posted
def getAllPostedTitles(date):
    s = '/'
    year, month, day = date.split('_')
    urlString = 'http://prowler333.herokuapp.com/articles/date' + s + year + s + month + s + day
    posted = req.get(urlString, auth=authentication)
    jsonString = posted.content
    articles = json.loads(jsonString)
    titles = list()
    for article in articles:
        titles.append(article["title"])
    return titles


# post all of today's articles
# three command line arguments
# first is path prefix (gives where the articles live)
# second is the number of articles in the current article dir
# third is the day
def main():
    # always specify the path to the webscraped directories
    prefix = str(sys.argv[1])
    #print prefix
    #today = prefix.split('/')
    today = str(sys.argv[3])
    year, month, day = today.split('_')
    # the number of articles in the directory
    n = int(sys.argv[2])

    # path building
    s = "/"

    # POST REQUEST ARGUMENTS
    url = "https://prowler333.herokuapp.com/articles/"
    imdatUrl = "https://prowler333.herokuapp.com/images/"
#    url = "http://localhost:" + str(port)  + "/"
    headers = {'content-type': 'application/json'}

    # get today's article titles to check if we have already posted
    titles = getAllPostedTitles(today)

    for i in range(0, n):
        filePath = prefix + s + "article_" + str(i) + ".txt"

        with open(filePath) as jsonFile:
            json_out = json.load(jsonFile)

            # if already in database, do not post!
            if json_out[0]["title"] in titles:
                continue

            # reformat the date
            json_out[0]['date'] = year + "-" + month + "-" + day + " " + "00:00:00"
            #print json_out
            #print "json to upload: " + json_out[0]["title"]
            # try-catch block
            try:
                #response = req.post(url, json=json_out, headers=headers)
                #json_out[0].pop("images", None)
                #print json_out[0]
                response = req.post(url, json=json_out[0], auth=authentication)
                # handle the status of posting
                status = response.status_code
                if status != 201:
                    print "NOT SUCCESSFUL POSTING ARTICLE: " + str(i) + " STATUS CODE: " + str(status)
                else:
                    print "SUCCESSFUL POSTING: " + json_out[0]["title"] + " IN PUBLICATION " + str(json_out[0]["publication"])
            except Exception:
                pass

            # now send the image urls separately
            responseData = json.loads(response.content)
            print len(responseData)

            # if the response fails, skip the rest, do not post any images
            if (len(responseData) == 1):
                continue

            # post all images associated with an article
            for iurl in json_out[0]['images']:
                if iurl is None:
                    continue
                else:
                    print "image: " + iurl
                    imJson = {'article' : responseData['id'], 'url': iurl}
                    try:
                        response = req.post(url = imdatUrl, json=imJson, auth=authentication)

                        # handle the status of posting
                        status = response.status_code
                        if status != 201:
                            print "NOT SUCCESSFUL POSTING IMAGE URL: " + imUrl + " STATUS CODE: " + str(status)
                    except Exception:
                        pass


if __name__=="__main__":
    main()
