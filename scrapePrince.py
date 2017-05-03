############################################################################################
# scrapePrince.py
#
#
# Author: Aamir Zainulabdeen
#
# Group: COS 333: Eric Hayes '18, Emily Tang '18, Fabian Lindfield Roberts '18
#
# The base methods for scraping the Daily Princetonian. See function comments for
# details.
############################################################################################

# dependencies
import sys
import requests as req
from bs4 import BeautifulSoup
import re # for the date, homeboy
import json
import time
import urllib2

# libraries written for prowler
import scrapeBase as sb

# globl vars defining the section URL structure
baseSectionURL = "http://www.dailyprincetonian.com/section/"
sections = ["news", "opinion", "sports", "street", "multimedia", "blog/intersections", "special", "editorial"]

# globl for the publication id of the daily princetonian
publicationId = sb.getPublicationId("prince")

"""
Output depends on switch. The default output is an encoded JSON string with
article title, date, author, and body (with the paragraphs joined by newlines
as defined in getBodyAsString(). If swtich is anyting else, the output is a list
with one dict containing the page (for testing purposes). The topic id is an integer
in the database, all of which are specified in formatDB.py and idFile.txt.
"""
def jsonify_page(urls, topicId, switch="JSON"):
    outlist = list()
    for url in urls:
        # download the page
        soup = sb.getSoup(url)

        # get the page content
        title = sb.listCatch(getTitle(soup))
        author = sb.listCatch(getAuthor(soup))
        date = getDate(soup)
        # get the image urls
        imageUrls = getImURLS(soup)
        # body comes in list of paragraphs
        body = grabPageText(soup)
        body = getBodyAsString(body)
        if (len(body) == 0):
            body = "/empty"
        # now convert to json dict
        bornAgain = {'title': title, 'author': author,
        'date': date, 'body': body,
        'images': imageUrls, 'url': url,
        'publication': publicationId, 'topic': topicId}
        outlist.append(bornAgain)

    if switch == "JSON":
        return json.dumps(outlist, sort_keys = True, indent = 4)
    else:
        return outlist

# utility testing
def testUrl(testUrl):
    # only download the page once
    soup = sb.getSoup(testUrl)

    # get the article title, time, author
    title = getTitle(soup)
    sys.stdout.write("Title:\t\t")
    sys.stdout.write(title[0].text)
    writeN()

    author = getAuthor(soup)
    sys.stdout.write("Author:\t\t")
    sys.stdout.write(author[0].text)

    date = getDate(soup)
    sys.stdout.write("\t\tDate:\t\t")
    sys.stdout.write(date)
    writeN()

    # get the body text of our soup
    body = grabPageText(soup)
    # print out the article body
    for p in body:
        sys.stdout.write(p.text)
        writeN()

def getBodyAsString(body):
    out = ""
    for p in body:
        out = out + p.text + "\n\n"
    return(out)

def main():
    testUrls = ["http://www.dailyprincetonian.com/article/2017/03/u-alum-organization-focuses-on-new-energy-sources",
                "http://www.dailyprincetonian.com/article/2017/03/editorial-affirming-free-speech-and-encouraging-team-leadership",
                "http://www.dailyprincetonian.com/article/2017/03/weber-talks-media-at-social-day"]

    for url in testUrls:
        testUrl(url)
        writeBreak()

# write break between articles
def writeBreak():
    sys.stdout.write('''\n\n
________________________________________________________________________________________
\n\n''')

# write newlines
def writeN():
    sys.stdout.write("\n\n")
    return

# grab the article title
def getTitle(soup):
    title = soup.select(".headline")
    return title

# grab the article author
def getAuthor(soup):
    author = soup.select(".author-line > a")
    return author

def getDate(soup):
    elements = soup.select(".author")
    # catch the list (if empty) then parse the date
    return sb.parseDate(sb.listCatch(elements))

# returns a list representation of a page's article body
def grabPageText(soup):
    # a list that contains all of the paragraphs in an article
    body = soup.select(".article-copy > p")
    return body

# get a list of all image urls in an article's soup
def getImURLS(soup):
    images = soup.select('.article-copy img')
    out = list()
    for im in images:
        out.append(im['src'])

    return out


# return a list of all article URLS from a query page
# params is a list of length three, the first element is
# the fromDate, second is toDate, third is query type
# dates are in the string format "mm/dd/yyyy"
# type is one of these possible strings: "article"; "media"; "post"
def getArticleURLS(params):
    qURL = getPrinceQURL(params[0], params[1], params[2])
    soup = sb.getSoup(qURL)
    links = soup.select(".clearfix a")
    urls = list()
    baseURL = "http://www.dailyprincetonian.com"
    # links are repeated, so we only select even indexes
    for i in range(0, len(links), 2):
        urls.append(links[i]['href'])

    for i in range(0, len(urls)):
        urls[i] = baseURL + urls[i]

    return urls

# construct a dated query string for articles
# a QURL is a query URL
# dates are in the string format "mm/dd/yyyy"
# type is one of these possible strings: "article"; "media"; "post"
def getPrinceQURL(fromDate, toDate, type):
    fromMonth, fromDay, fromYear = fromDate.split("/")
    toMonth, toDay, toYear = toDate.split("/")

    # query string params
    baseURL = "http://www.dailyprincetonian.com/search/"
    fromMonthBase = "?a=1&s=&ti=&ts_month="
    fromDayBase = "&ts_day="
    fromYearBase = "&ts_year="
    toMonthBase = "&te_month="
    toDayBase = "&te_day="
    toYearBase = "&te_year="
    typeBase = "&au=&tg=&ty="
    endURL = "&o=date"

    construction = baseURL + fromMonthBase + fromMonth
    construction = construction + fromDayBase + fromDay
    construction = construction + fromYearBase + fromYear + toMonthBase
    construction = construction + toMonth + toDayBase + toDay
    construction = construction + toYearBase + toYear + typeBase + type + endURL

    return construction

# DEBUG :: DEPRECATED AS API of jsonify_page() has changed
# get today's articles in a list of JSON's using the time module
# def getTodaysArticles():
#     today = time.strftime("%m/%d/%Y")
#     # get today's articles
#     urls = getArticleURLS([today, today, "article"])
#     outputJSON = list()
#     for url in urls:
#         outputJSON.append(jsonify_page(url))
#
#     return outputJSON

# # get a specific date's articles as a list of JSONS
# def getDatesArticles(date):
#     # get today's articles
#     urls = getArticleURLS([date, date, "article"])
#     outputJSON = list()
#     for url in urls:
#         outputJSON.append(jsonify_page(url))
#
#     return outputJSON


# run main
if __name__ == "__main__":
    main()
