"""
scrapeTigerMag.py

Author: Aamir Zainulabadeen

Scrape the contents of the Tiger magazine @ http://www.tigermag.com/

"""
import json

# prowler dependencies
import scrapeBase as sb

# DEBUG
# read in the publicationId from the master file
publicationId = sb.getPublicationId("tigerMag")

# fulfill the scrapeBase API
# topicId is a list of topics
def jsonify_page(urls, topicId, switch="JSON"):
    outlist = list()
    for url in urls:
        # download the page
        soup = sb.getSoup(url)

        # get the page content
        title = getTitle(soup)
        author = getAuthor(soup)
        date = getDate(soup)
        # get the image urls
        imageUrls = getImURLS(soup)
        # body comes in list of paragraphs
        body = getBody(soup)

        # now convert to json dict
        bornAgain = {'title': title, 'author': author,
        'date': date, 'body': body,
        'images': imageUrls, 'url': url,
        'publication': publicationId, 'topic': topicId,
        'posted': False, 'id': 0}
        outlist.append(bornAgain)

    if switch == "JSON":
        return json.dumps(outlist, sort_keys = True, indent = 4)
    else:
        return outlist

# select the url to direct to based on topic
# defaults to news (see else at end of function)
def selectTopicPage(name):
    if name == "Princeton":
        return 'http://www.tigermag.com/category/princeton/'
    elif name == "Advice":
        return 'http://www.tigermag.com/category/life/advice-life/'
    elif name == "Letters":
        return 'http://www.tigermag.com/category/letters-2/'
    elif name == "News":
        return 'http://www.tigermag.com/category/news-2/'
    else:
        return 'http://www.tigermag.com/category/news-2/'

# fulfill the scrapeBase API
# get all urls for a current date
# currently does not depend on Date, fix!
def getAllUrls(date, topics):
    # bind urls and topics
    outData = list()
    for topic in topics:
        todayUrls = getTopicPageUrls(selectTopicPage(topic['name']))
        outData.append([topic, todayUrls])
    return outData

# get all the urls from a topic page
def getTopicPageUrls(topicPage):
    soup = sb.getSoup(topicPage)
    elements = soup.select(".post a")

    outSet = set()
    for el in elements:
        outSet.add(el["href"])

    return list(outSet)

# for an article's soup, get the title
def getTitle(soup):
    dirtyTitle = soup.select(".hentry-meta h1")
    title = sb.listCatch(dirtyTitle)
    return title

# for an article's soup, get the date
def getDate(soup):
    dirtyDate = soup.select(".hentry-meta p")
    date = sb.listCatch(dirtyDate)
    # now sanitize the date
    clean = sb.parseDate(date)
    return clean

# for an article's soup, get the author:
def getAuthor(soup):
    body = soup.select(".hentry-content p")
    if len(body) != 0:
        dtitle = [body[-1]]
        title = sb.listCatch(dtitle)
        return title
    else:
        return "/empty"

# for an article's soup, get the body:
def getBody(soup):
    body = soup.select(".hentry-content p")
    outText = ""
    for b in body:
        outText = outText + sb.listCatch([b]) + "\n\n"
    return outText

# get all of the image urls
def getImURLS(soup):
    images = soup.select('.hentry-content img')
    out = list()
    for im in images:
        out.append(im['src'])

    return out
