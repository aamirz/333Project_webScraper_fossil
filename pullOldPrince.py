"""
pullOldPrince.py

Just pull the Prince for our database!

Aamir Zainulabadeen

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
# c is the separating character
def gta_reformat(date, c):
    month, day, year = date.split("/")
    return year + c + month + c + day

# make the save path for today's article
def savePath(prefix, publication, today):
    s = "/"
    spath = prefix + s + publication + s + gta_reformat(today, '_')
    return spath

# takes two command line args, the first is the prefix to the parent of saving
# dir, the second is the day's date (if we want to pull a day other than today)
def main():
    ## the first command line arg is the prefix to the saving directory
    prefix = str(sys.argv[1])
    if len(sys.argv) < 3:
        today = time.strftime("%m/%d/%Y")
    else:
        today = str(sys.argv[2])

    if len(sys.argv) < 2:
        print "you need a saving directory!"
        return 0

    # pull the daily princetonian
    print "pulling... "
    nPrince = sb.pull(publication="prince", date=today, FgetUrls=sp.getPrinceUrls,
    Fjsonify=sp.jsonify_page, saveDir=savePath(prefix, "prince", today))


if __name__=="__main__":
    main()
