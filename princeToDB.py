"""
postScrapedArticle.py
Author: Aamir Zainulabadeen

POSTS an article to our database.
"""
import sys
import scrapePrince as sp
import requests as req
import json

# scrape an article with url and post it
def postOne(pageUrl, port):
    js = sp.jsonify_page(url = pageUrl)

    # POST REQUEST
    url = "http://localhost:" + port  + "/"
    headers = {'content-type': 'application/json', 'User-Agent': 'my app'}
    # try-catch block
    try:
        response = req.post(url, json=js, headers=headers)
    except Exception:
        pass


# post all of today's articles 
# three command line arguments
# first is path prefix
# second is the number of articles in the current article dir
# third is the port number (optional)
def main():
    # always specify the path to the webscraped directories
    prefix = str(sys.argv[1])
    
    # the number of articles in the directory
    n = int(sys.argv[2])
    
    # the default port is 8080
    if len(sys.argv) < 4:
        port = 8080
    else:
        port = int(sys.argv[3]) 

    # path building
    s = "/"

    # POST REQUEST ARGUMENTS
    url = "http://localhost:" + str(port)  + "/"
    headers = {'content-type': 'application/json', 'User-Agent': 'my app'}
    
    for i in range(0, n):
        filePath = prefix + s + "article_" + str(i) + ".txt"

        with open(filePath) as jsonFile:
            json_out = json.load(jsonFile)
            print json_out
            # try-catch block
            try:
                response = req.post(url, json=json_out, headers=headers)
            except Exception:
                pass


#     url = "http://www.dailyprincetonian.com/article/2017/03/park-president-impeached"
#     js = sp.jsonify_page(url = url)
#     with open('sampleArticle.json', 'w') as outfile:
#         json.dump(js, outfile)
#         postOne(url, port)


if __name__=="__main__":
    main()
