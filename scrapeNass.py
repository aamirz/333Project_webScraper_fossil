"""
scrapeNass.py

Functions to facilitate pulling nassau weekly aritcles.
TODO: extend this scraping/database to include the verbatim section

Aamir Zainulabadeen
"""
import json
import re
import scrapeBase as sb

# pull the id from the master table
publicationId = sb.getPublicationId("nass")

"""
Output depends on switch. The default output is an encoded JSON string with
article title, date, author, and body (with the paragraphs joined by newlines).
If swtich is anyting else other than JSON, the output is a list
with one dict containing the page (for testing purposes).
"""
def jsonify_page(urls, topicId, switch="JSON"):
    outlist = list()

    for url in urls:
        soup = sb.getSoup(url)

        title = getTitle(soup)
        author = getAuthor(soup)
        date = getDate(soup)
        imageUrls = getImages(soup)
        body = getBody(soup)
        # now convert to json dict, publication should correspond to nass, topic should be misc
        bornAgain = {'title': title, 'author': author, 'date': date, 'body': body,
            'images': imageUrls, 'url': url, 'publication': publicationId, 'topic': topicId,
            "posted": False, "id": 0}
        outlist.append(bornAgain)

    if switch == "JSON":
        return json.dumps(outlist, sort_keys = True, indent = 4)
    else:
        return outlist



# build a title specifically in the format of the nassau weekly
def buildTitle(elements):
    core = elements[6:-4]
    s = " "
    build = ""
    # build the out string
    i = 0
    for el in core:
        if i == 0:
            build = build + el
            i = 1
        else:
            build = build + s + el
    return build

# get the title from our soup, gives formatted string
# or "/empty"
def getTitle(soup):
    element = soup.select(".post-meta h1")
    dirtyTitle = sb.listCatch(element)
    if dirtyTitle != "/empty":
        return buildTitle(dirtyTitle.split(" "))
    else:
        return dirtyTitle

# get the author from our soup
def getAuthor(soup):
    element = soup.select(".post-author")
    # if the author field is empty, return "/empty"
    return sb.listCatch(element)


# get the date from our soup, format it nicely for the database
def getDate(soup):
    element = soup.select(".post-date")
    # if the date field is empty, return "/empty"
    dirtyDate = sb.listCatch(element)
    if dirtyDate != "/empty":
        return sb.parseDate(dirtyDate)
    else:
        return dirtyDate

# get the body of text from the input
def getBody(soup):
    # get all the text from the page
    #content = soup.select(".post-content .s1")
    #content = soup.select(".post-content p")
    # join it all in one body
    body = ""
    s = " \n "
    # for con in content:
    #     body = body + s + con.text

    #if body == "":
    content = soup.select(".post-content p")
    for con in content:
        body = body + s + con.text

    if body == "":
        return "/empty"

    return body


# get the images from our soup and associated captions, return a dict
# can extend to get captions
def getImages(soup):
    elements = soup.select(".post-content img")
    # a list of image urls
    urls = list()
    for el in elements:
        urls.append(el["src"])
    return urls

# get the verbatim as one block string
def getVerbatim(issueSoup):
    elements = issueSoup.select(".issue-verbatim")

    # join all of the vermatims
    s = " \n "
    verbatim = ""
    for el in elements:
        verbatim = verbatim + s + el.text
    return verbatim

# get all the articles in an issue
def getIssueArticleUrls(issueUrl):
    soup = sb.getSoup(issueUrl)
    elements = soup.select(".issue-posts span a")
    i = 0
    urls = list()
    # every other element is an author link
    # so only extract the odd elements
    for el in elements:
        url = el["href"]
        # exclude the author links
        found = re.search("/byline/", url)
        if found is None:
            urls.append(url)
    return urls

# get all the issue urls / dates from the archival page of the nass
# returns a list of len == 2, with the first element as list of urls
# the second element in the returned list is a list of dates
# NOTE: can use the datetime module when pulling to only pull new issues, on daily check!
def getArchiveIssueLinks(archiveUrl="http://www.nassauweekly.com/issue/"):
    soup = sb.getSoup(archiveUrl)
    elements = soup.select("div h2 a")
    issueUrls = list()
    for el in elements:
        issueUrls.append(el["href"])
    # grab the dates as well!
    elements = soup.select(".post-date")
    dates = list()
    for el in elements:
        dates.append(sb.parseDate(el.text).split(" ")[0])
    return [issueUrls, dates]


# Return all the issues that are the same as a given date
# date is of the form YYYY-MM-DD
def getBeyondDatIssues(date):
    # pull links and dates
    urlDat = getArchiveIssueLinks()
    urls = urlDat[0]
    dates = urlDat[1]

    # collect the indexes of all valid dates
    i = 0
    iwanted = list()
    for dat in dates:
        # if the issue came out on or before our date
        # the direct string comparison works
        if date == dat:
            iwanted.append(i)

        # increment our counter
        i = i + 1
    urlWanted = list()

    # collect all valid urls
    for i in iwanted:
        urlWanted.append(urls[i])

    # return the issue urls
    return urlWanted

# get all the articles beyond a certain date
# date is in YYYY-MM-DD format
# the topic argument completes the scrapeBase API but is not needed
# for the nassau weekly
def getNassUrls(date, topics):
    # get the issues beyond
    issues = getBeyondDatIssues(date)

    # now for each issue get all of the articles urls
    urls = list()
    for issue in issues:
        urls = urls + getIssueArticleUrls(issue)

    # bind the urls to topics (there should only be one)
    topic = topics[0]
    outData = list()
    outData.append([topic, urls])

    # return all of the urls
    return outData
