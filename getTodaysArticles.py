"""
getTodaysArticles.py

Author: Aamir Zainulabadeen

simple script to pull today's articles from the daily princetonian (dailyprincetonian.com) and save them to txt and json files
"""
import sys
import time
import scrapePrince as sp
import json


def gta_reformat(date):
    month, day, year = date.split("/")
    return year + "_" + month + "_" + day

# takes two comman line args, the first is the prefix to the parent of saving
# dir, the second is the day's date 
def main():
    ## the first command line arg is the prefix to the saving directory
    prefix = str(sys.argv[1])
    s = "/"
    if len(sys.argv) < 3:
        today = time.strftime("%m/%d/%Y")
    else:
        today = str(sys.argv[2])
    todayUrls = sp.getArticleURLS([today, today, "article"])
    # outputJSON = list()
    i = 0
    
    if len(sys.argv) < 3:
        today = time.strftime("%Y_%m_%d")
    else:
        today = gta_reformat(sys.argv[2])
    for url in todayUrls:
        print url + "\n"
        #outputJSON.append(sp.jsonify_page(url))
        jsonOut = sp.jsonify_page(url)
        with open(prefix + s + today + s + "article_" + str(i) + ".txt", "w") as outfile:
            json.dump(jsonOut, outfile)
        i = i + 1
    print "pulling today's articles successful"


    # with open(prefix + s +  today + s + "articles.txt", "w") as outfile:
    # json.dump(outputJSON, outfile)
    print "write successful"

if __name__=="__main__":
    main()
    
