"""
getTodaysArticles.py

Author: Aamir Zainulabadeen

simple script to pull today's articles from all publications
and save them to txt files as json

"""
import sys
import time
import json
import os
import errno

# libraries written for prowler
import scrapeBase as sb
import scrapePrince as sp
import scrapeNass as sn

# reformat the data from the input
def gta_reformat(date):
    month, day, year = date.split("/")
    return year + "_" + month + "_" + day


# takes two command line args, the first is the prefix to the parent of saving
# dir, the second is the day's date (if we want to pull a day other than today)
def main():
    ## the first command line arg is the prefix to the saving directory
    prefix = str(sys.argv[1])
    s = "/"
    if len(sys.argv) < 3:
        today = time.strftime("%m/%d/%Y")
    else:
        today = str(sys.argv[2])

    if len(sys.argv) < 2:
        print "you need a saving directory!"
        return 0

    # pull the daily princetonian
    sb.pull(publication="prince", date=today, FgetUrls=sp.getPrinceUrls,
    Fjsonify=sp.jsonify_page, saveDir=prefix)


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
