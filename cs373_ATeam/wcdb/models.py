import os
os.environ["DJANGO_SETTINGS_MODULE"] = "cs373_ATeam.settings"
from django.db import models

# Create your models here.

#general method for adding to a list
def list_add(list, id) :
    list.append(id)


#class for the ListType complexType
class Li() :
    #Li
    def __init__(self):
        href          = None
        embed         = None
        text          = None
        #text not in the attributes; not Li
        floating_text = None

    def populate(self, e_node) :
        href          =  e_node.get("href")
        embed         = e_node.get("embed")
        text          =  e_node.get("text")
        floating_text =         e_node.text


class Common() :
    #Common
    def __init__(self):
        self.citations      = []
        external_links = []
        images         = []
        videos         = []
        maps           = []
        feeds          = []
        #similar to floating text
        summary        = None

    def populate(self, e_node) :
        for citation in e_node.find("Citations") :
            temp_li = Li()
            temp_li.populate(citation)
            self.citations.append(temp_li)

        for link in e_node.find("ExternalLinks") :
            temp_li = Li()
            temp_li.populate(link)
            self.citations.append(temp_li)

        for image in e_node.find("Images") :
            temp_li = Li()
            temp_li.populate(image)
            self.citations.append(temp_li)

        for video in e_node.find("Videos") :
            temp_li = Li()
            temp_li.populate(video)
            self.citations.append(temp_li)

        for map in e_node.find("Maps") :
            temp_li = Li()
            temp_li.populate(map)
            self.citations.append(temp_li)

        for feed in e_node.find("Feeds") :
            temp_li = Li()
            temp_li.populate(feed)
            self.citations.append(temp_li)

        summary = e_node.find("Summary").text



class Crisis(models.Model) :
    crisis_ID         = models.CharField(max_length=200)
    name              = models.CharField(max_length=200)
    kind              = models.CharField(max_length=200)
    date              = models.CharField(max_length=200)
    time              = models.CharField(max_length=200)
    people            = []
    organizations     = []
    #Li list
    #locations, human_impact, economic_impact is always floating text
    locations         = []
    human_impact      = []
    economic_impact   = []
    resources_needed  = []
    ways_to_help      = []
    #common
    common            = Common()


class Person(models.Model) :
    person_ID         = models.CharField(max_length=200)
    name              = models.CharField(max_length=200)
    kind              = models.CharField(max_length=200)
    location          = models.CharField(max_length=200)
    common            =                         Common()
    crises            = []
    organizations     = []
    

class Org(models.Model) :
    org_ID      = models.CharField(max_length=200)
    name        = models.CharField(max_length=200)
    kind        = models.CharField(max_length=200)
    location    = models.CharField(max_length=200)
    crises      = []
    people      = []
    #Li list
    history     = []
    contact     = []
    #Common
    common      = Common()



