"""
getTodaysArticles.py

Author: Aamir Zainulabadeen

simple script to pull today's articles from the daily princetonian (dailyprincetonian.com) and save them to txt and json files
"""
import sys
import time
import scrapePrince as sp
import json
import os
import errno

# libraries written for prowler
import scrapeBase as sb

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

############## ARTICLE FULL SCRAPE :: ADDED IMAGE VIRTUAL SCRAPE TO SP.JSONIFY ###########################
    # get the article urls for the given day
    todayUrls = sp.getArticleURLS([today, today, "article"])

    if len(sys.argv) < 3:
        today = time.strftime("%Y_%m_%d")
    else:
        today = gta_reformat(sys.argv[2])

    # separate file for each article
    i = 0
    for url in todayUrls:
        #print url + "\n"
        jsonOut = sp.jsonify_page([url])
        with open(prefix + s + today + s + "article_" + str(i) + ".txt", "w") as outfile:
            outfile.write(jsonOut)
        i = i + 1

############ IMAGE FULL SCRAPE #######################################
#     i = 0
#     for url in todayUrls:
#         imPath = prefix + s + today + s + "article_" + str(i) + "images/"
#         # check if the image directory exists for an article
#         make_sure_path_exists(imPath)
#         # update the counter
#         i = i + 1
#         # now get all images with this url
#         soup = sb.getSoup(url)
#         imUrls = sp.getImURLS(soup)
#         # save each image to an appropriate file
#         k = 0
#         for url in imUrls:
#             image = sp.getImage(url)
#             sp.writeImageToFile(image, imPath + "image_" + str(k) + ".jpeg")
#             k = k + 1

    # pool all articles into one thing!
#     articles = sp.jsonify_page(todayUrls)
#     with open(prefix + s + today + s + "allArticles.txt", "w") as outfile:
#         outfile.write(articles)
#         print "pooling all articles successful"
#     print "pulling today's articles successful"


# function to make a new directory taken from stackoverflow answer #2
# http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if __name__=="__main__":
    main()
