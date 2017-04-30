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
    today = prefix.split('/')
    today = today[1]
    year, month, day = today.split('_')
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
    url = "https://prowler333.herokuapp.com/articles/"
    imdatUrl = "https://prowler333.herokuapp.com/images/"
#    url = "http://localhost:" + str(port)  + "/"
    headers = {'content-type': 'application/json'}
    
    for i in range(0, n):
        filePath = prefix + s + "article_" + str(i) + ".txt"
        
        with open(filePath) as jsonFile:
            json_out = json.load(jsonFile)
            # reformat the date
            json_out[0]['date'] = year + "-" + month + "-" + day + " " + "00:00:00"
            #print json_out
            #print "json to upload: " + json_out[0]["title"]
            # try-catch block
            try:
                #response = req.post(url, json=json_out, headers=headers)
                response = req.post(url, json=json_out[0])
                # handle the status of posting
                status = response.status_code
                if status != 201:
                    print "NOT SUCCESSFUL POSTING ARTICLE: " + str(i) + " STATUS CODE: " + str(status)
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
                        response = req.post(url = imdatUrl, json=imJson)
                        
                        # handle the status of posting
                        status = response.status_code
                        if status != 201:
                            print "NOT SUCCESSFUL POSTING IMAGE URL: " + imUrl + " STATUS CODE: " + str(status)
                    except Exception:
                        pass


#     url = "http://www.dailyprincetonian.com/article/2017/03/park-president-impeached"
#     js = sp.jsonify_page(url = url)
#     with open('sampleArticle.json', 'w') as outfile:
#         json.dump(js, outfile)
#         postOne(url, port)


if __name__=="__main__":
    main()
