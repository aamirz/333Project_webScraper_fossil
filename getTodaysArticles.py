"""
getTodaysArticles.py

Author: Aamir Zainulabadeen

simple script to pull today's articles from the daily princetonian (dailyprincetonian.com) and save them to txt and json files
"""
import sys
import time
import scrapePrince as sp
import json

def main():
    ## the first command line arg is the prefix to the saving directory
    prefix = str(sys.argv[1])
    today = time.strftime("%m/%d/%Y")
    todayUrls = sp.getArticleURLS([today, today, "article"])
    outputJSON = list()
    for url in todayUrls:
        outputJSON.append(sp.jsonify_page(url))
    print "pulling today's articles successful"

    today = time.strftime("%Y_%m_%d")
    with open(prefix + "/" +  today + "/" + "articles.txt", "w") as outfile:
        json.dump(outputJSON, outfile)
    print "write successful"

if __name__=="__main__":
    main()
