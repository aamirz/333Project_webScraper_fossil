"""
scrapeNass.py

Functions to facilitate pulling nassau weekly aritcles.
TODO: extend this scraping/database to include the verbatim section

Aamir Zainulabadeen
"""
import json
import re
import scrapeBase as sb

"""
Output depends on switch. The default output is an encoded JSON string with
article title, date, author, and body (with the paragraphs joined by newlines).
If swtich is anyting else other than JSON, the output is a list
with one dict containing the page (for testing purposes).
"""
def jsonify_page(urls, switch="JSON"):
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
            'images': imageUrls, 'url': url, 'publication': 2, 'topic': 2}
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
    for el in core:
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
    content = soup.select(".post-content .s1")

    # join it all in one body
    body = ""
    s = " \n "
    for con in content:
        body = body + s + con.text
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
