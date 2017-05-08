""""
formatDB.py
Aamir Zainulabadeen
COS 333 Project : Prowler Application

Format the database with both topics and publications.
"""
import sys
import requests as req
from requests.auth import HTTPBasicAuth
import json

# prowler dependencies
import scrapeBase as sb

# globl to access database
# authentication for posting to database
authentication = HTTPBasicAuth('aamirz', 'aamirziscool')

class Publication:
    # make a new publication object
    def __init__(self, name, logo, description):
      self.name = name
      self.logo = logo
      self.description = description
      self.topics = list()

    # add the id to our structure
    def addId(self, id):
        self.id = id

    # add a new topic to our list
    # dict in form {"name": , "description": }
    def addTopic(self, topic):
        self.topics.append(topic)

    # jsonify our publication object
    def jsonify(self):
        born = {'name': self.name, 'logo': self.logo, 'description': self.description}
        return born

    # post a publication to the given url
    def ppost(self):
        url = 'http://prowler333.herokuapp.com/publications/'
        status = 0
        try:
            #response = req.post(publicationPostUrl, json=prince.jsonify(), auth=authentication)
            #response = req.post(publicationPostUrl, json=json.load(prince.jsonify()), auth=authentication)
            response = req.post(url, json=self.jsonify(), auth=authentication)
            #response = req.post(url=publicationPostUrl, json="{'name': 'lovley', 'logo':'warren', 'description':'is Mayor'}", auth=authentication)
            # handle the status of posting
            status = response.status_code
            if status != 201:
                print "NOT SUCCESSFUL POSTING Publication: " + self.name + " STATUS CODE: " + str(status)
            else:
                print "SUCCESSFUL"
        except Exception:
            print "BAD REQUEST FOR PUBLICATION POSTING ON: " + self.name
            pass

        return json.loads(response.content)["id"]

    # post a topic to the database
    def topicPost(self, topic):
        url = 'http://prowler333.herokuapp.com/topics/'
        status = 0
        try:
            response = req.post(url, json=topic, auth=authentication)
            status = response.status_code
            if status != 201:
                print "NOT SUCCESSFUL POSTING Publication: " + self.name + " STATUS CODE: " + str(status)
            else:
                print "SUCCESSFUL"
        except Exception:
            print "BAD REQUEST FOR PUBLICATION POSTING ON: " + self.name
            pass

        return {'name' : topic['name'], 'id' : json.loads(response.content)["id"]}

# post The Prince as a publication to the database
def postPrince():
    # get the daily prince info from source
    princeUrl = 'http://www.dailyprincetonian.com/'
    princeSoup = sb.getSoup(princeUrl)
    princeAboutUrl = 'http://www.dailyprincetonian.com/page/about'
    princeAboutSoup = sb.getSoup(princeAboutUrl)

    # for now we are using the old logo because the new one looks nasty
    prince = Publication(name="The Daily Princetonian",
    #logo=sb.listCatchItem(princeSoup.select(".col-md-8 a img"))["src"],
    logo = 'http://dirgyzwl2hnqq.cloudfront.net/20170330XJxw8OoJDm/dist/img/favicons/apple-touch-icon.png',
    description=sb.listCatchItem(princeAboutSoup.select(".col-sm-12 p")).text)
    id = prince.ppost()
    print "prince id: " + str(id)
    prince.addId(id)
    return prince

# post the publication information for the Nassau Weekly
def postNass():
    # get the nass's data from source
    nassUrl = 'http://www.nassauweekly.com/'
    nassSoup = sb.getSoup(nassUrl)
    nassAboutUrl = 'http://www.nassauweekly.com/about/'
    nassAboutSoup = sb.getSoup(nassAboutUrl)

    # the logo
    #elements = nassSoup.select(".logo img")
    #el = sb.listCatchItem(elements)
    #logo = el["src"]
    logo = 'https://walkercarpenter.files.wordpress.com/2016/02/nass-circle.png?w=800'

    # about
    elements = nassAboutSoup.select(".post-content p")
    about = ""
    s = " \n "
    i = 0
    # shortened it as database would not accept long strings
    for p in elements:
        if i == 2:
            break
        about = about + s + p.text
        i = i + 1
    print "PRINTING ABOUT LEN: "
    print len(about)
    nass = Publication(name="The Nassau Weekly", logo = logo, description = about)
    id = nass.ppost()
    print "nass id: " + str(id)
    nass.addId(id)
    return nass

# construct all of the prince topic ids
def postPrinceTopics(prince):
    if prince is None:
        print "ERROR IN POSTPRINCETOPICS, PRINCE IS NONE"
        exit()

    princeTopics = [{'name': "News", 'description': "The most current events on Princeton's campus."},
    {'name': "Opinion", 'description': "Important perspectives from around Princeton's campus."},
    {'name': "Sports", 'description': "The latest on our Tigers' atheltic feats."},
    {'name': 'Street', 'description': "The day to day on campus events, fashion, and more."},
    {'name': 'Blog', 'description': "Hear the most creative voices on campus."},
    {'name': 'Editorial', 'description': "The editorial board weighs in on important issues."}]

    princeTopicIds = list()
    princeTopicIds.append({"publication": "prince"})
    for topic in princeTopics:
        princeTopicIds.append(prince.topicPost(topic))
        prince.addTopic(topic)

    return princeTopicIds


# construct all of the nassau weekly topic ids
def postNassTopics(nass):
    if nass is None:
        print "ERROR in POSTNASSTOPICS, NASS IS NONE"
        exit()
    humor = {'name': 'The Nassau Weekly', 'description': 'all things funny in Princeton and beyond'}
    nass.addTopic(humor)

    nassTopicIds = list()
    nassTopicIds.append({"publication": "nass"})
    for topic in nass.topics:
        nassTopicIds.append(nass.topicPost(topic))

    return nassTopicIds


# run all the utilities
def main():
    # format all the publication content
    prince = postPrince()
    nass = postNass()
    masterTable = {"prince": prince.id, "nass": nass.id}

    ## now do this for the nass!
    princeTopicIds = postPrinceTopics(prince)
    # princeOutData = [{"name": "prince"}, prince.topics, princeTopicIds]
    #print princeTopicIds
    nassTopicIDs = postNassTopics(nass)
    # nassOutData = [{"name":"nass"}, nass.topics, nassTopicIDs]

    # outData = [masterTable, princeOutData, nassOutData]
    outData = [masterTable, princeTopicIds, nassTopicIDs]
    # a master table of all the publications
    jsonOut = json.dumps(outData, sort_keys = True, indent = 4)
    # save each publication id for future use
    with open("idFile.txt", "w") as outf:
        outf.write(jsonOut)



if __name__=="__main__":
    main()
