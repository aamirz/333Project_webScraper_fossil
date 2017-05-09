"""
# scrapeBase.py
#
# Author: Aamir Zainulabadeen
#
# Base functions to be used by all of the scraping scripts.
"""
import sys
import json
import requests as req
from bs4 import BeautifulSoup
import re # for the date homeboy

# download the page
def getSoup(pageURL):
    page = req.get(pageURL)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

######### date conversions ################

# globl var defining date syntax for daily princetonian, nassau weekly, etc.
dateRE = '''(Jan |Feb |Mar |Apr |May |Jun |Jul |Aug |Sep |Oct |Nov |Dec )([1-9]|[12][0-9]|[3][01]), [2-9][0-9][0-9][0-9]'''


# convert the month to a formatted string for database
def monthConvert(month):
    conversion = { "Jan": '01',
                   "Feb": '02',
                   "Mar": '03',
                   "Apr": '04',
                   "May": '05',
                   "Jun": '06',
                   "Jul": '07',
                   "Aug": '08',
                   "Sep": '09',
                   "Oct": '10',
                   "Nov": '11',
                   "Dec": '12'
                   }
    return conversion[month]

# convert the day from a specified string
def dayConvert(day):
    if len(day) < 2:
        return "0" + day
    else:
        return day

# convert the date from format 'Mar 4 2017' to '2017-03-04 00:00:00'
def convertDate(date, c):
    month, day, year = date.split(c)
    nMonth = monthConvert(month)
    day = dayConvert(day[0:-1])
    s = "-"
    return year + s + nMonth + s + day + " " + "06:00:00" # default time

# parse the date string, select the month day and year
def parseDate(date):
    if date != "/empty":
        found = re.search(dateRE, date)
        if found is None:
            return "/empty"
        elect = found.group(0)
        return convertDate(elect, " ")
    else:
        return "/empty"


# small function to catch empty lists of bs4 html objects
# gets the first object in the bs4 list
def listCatch(aList):
    if len(aList) == 0:
        return "/empty"
    else:
        return aList[0].text

# catch the first item in a list and return it
def listCatchItem(aList):
    if len(aList) == 0:
        return "/empty"
    else:
        return aList[0]

# get the publication id from the master table
def getPublicationId(publication):
    if publication is None:
        print "Bad publication field in getPublicationId!"
        return 0

    # read in the file
    id = 0
    with open("idFile.txt") as idF:
        masterTable = json.load(idF)
        id = masterTable[0][publication]
    return id

# get the publication topics from the master table
# return a list of dicts that hold the topic ids and topics
def getPublicationTopics(publication):
    if publication is None:
        print "Bad publication field in getPublicationId!"
        return 0

    # read in the master table file
    id = 0
    with open("idFile.txt") as idF:
        masterTable = json.load(idF)
        # search the master table
        for i in range(1, len(masterTable)):
            if masterTable[i][0]["publication"] == publication:
                return masterTable[i][1:]

        # if the fail the search, return -1
        return -1

# pull the entire publication that is passed with these params
# url topic list is a list of lists that contain the topic as the
# first element and the rest of the list is string urls
# Fjsonify is a function that jsonifys an url
# saveDir is the directory in which to save the pages pulled
def publicationPull(urlTopicList, Fjsonify, saveDir):
    # param for naming each article
    i = 0
    titleList = list()
    for urlTopic in urlTopicList:
        topic = urlTopic[0]
        for url in urlTopic[1]:
            # the function takes a list of urls as a
            # general argument, but our database only
            # accepts one post at a time
            json_out = Fjsonify(urls=[url], topicId=topic["id"])
            title = json.loads(json_out)[0]['title']
            # if we have already saved this article, continue
            if (title in titleList):
                continue

            # otherwise, save the article and record the title
            titleList.append(title)
            fPath = saveDir + '/' + "article_" + str(i) + ".txt"
            with open(fPath, "w") as outF:
                outF.write(json_out)
            i = i + 1

    return i

# Pulls the given resource for the given publication (str)
# FgetUrls (function to get the urls for this publication),
# Fjsonify (function to jsonify the given urls) and saves to saveDir,
# date (str:: 'mm/dd/yyyy'),
# The return value is a count of the articles pulled
def pull(publication, date, FgetUrls, Fjsonify, saveDir):
    # get the topics for this publication
    topics = getPublicationTopics(publication)
    # get the url topic list for this date
    utList = FgetUrls(date=date, topics=topics)
    # get the articles for these urls and save them in saveDir
    count = publicationPull(urlTopicList=utList, Fjsonify=Fjsonify, saveDir=saveDir)

    return count
