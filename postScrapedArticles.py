"""
postScrapedArticles.py
Author: Aamir Zainulabadeen

POSTS articles to our database. Needs only for the article files to be
named and formatted correctly, simply uploads all articles of today that
have not been already posted to the database.
"""
import sys
import re
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


# say whether two titles match, ignore spaceing issues
def doesMatch(a, b):
    if re.match(a, b) is None:
        return False
    else:
        return True

# say whether any of the article titles match this one
def titleExists(title, titleList):
    for t in titleList:
        if doesMatch(title, t):
            return True
    # if we pass the forloop, it is not found in the list
    return False

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
            json_out[0]['date'] = year + "-" + month + "-" + day + " " + "06:00:00"
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
                    print "NOT SUCCESSFUL POSTING ARTICLE:\t " + str(i) + "\t STATUS CODE: \t" + str(status)
                else:
                    print "SUCCESSFUL POSTING:\t " + json_out[0]["title"] + "\t IN PUBLICATION \t" + str(json_out[0]["publication"])
                    #json_out[0]["posted"] = True
                    #json_out[0]["id"] = response.content[0]['id']
            except Exception:
                pass

            # now send the image urls separately
            responseData = json.loads(response.content)
            print len(responseData)

            # if the response fails, skip the rest, do not post any images
            if (responseData.get('id', "BLAH") == "BLAH"):
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
