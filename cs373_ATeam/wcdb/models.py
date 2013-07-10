import os
os.environ["DJANGO_SETTINGS_MODULE"] = "cs373_ATeam.settings"
from django.db import models
#from unloadModels import xml_from_li

# Create your models here.

#general method for adding to a list
def list_add(list, id) :
    #print "BEFORE APPEND", list
    list.append(id)
    #print "AFTER APPEND", list


#class for the ListType complexType
class Li() :
    #Li
    href          = None
    embed         = None
    text          = None
    #text not in the attributes; not Li
    floating_text = None
    def __init__(self):
        href          = None
        embed         = None
        text          = None
        #text not in the attributes; not Li
        floating_text = None

    def populate(self, e_node) :
        self.href          =  e_node.get("href")
        self.embed         = e_node.get("embed")
        self.text          =  e_node.get("text")
        self.floating_text =         e_node.text

    def print_xml (self) :
        #Export xml from the li class
        self_string = ""
        if self is not None:
            if self.href is not None :
                self_string += "<li> href=\"" + self.href + "\"</li>"
            if self.embed is not None :
                self_string += "<li> embed=\"" + self.embed + "\"</li>"
            if self.text is not None :
                self_string += "<li>" + self.text + "</li>"
            if self.floating_text is not None :
                self_string += "<li>" + self.floating_text + "</li>"
        #Conclude li xml instance string
        return self_string



class Common() :
    #Common
    citations      = []
    external_links = []
    images         = []
    videos         = []
    maps           = []
    feeds          = []
    #similar to floating text
    summary        = None
    def __init__(self):
        self.citations      = []
        self.external_links = []
        self.images         = []
        self.videos         = []
        self.maps           = []
        self.feeds          = []
        #similar to floating text
        self.summary        = None

    def populate(self, e_node) :
        for citation in e_node.find("Citations") or [] :
            temp_li = Li()
            temp_li.populate(citation)
            self.citations.append(temp_li)

        for link in e_node.find("ExternalLinks") or [] :
            temp_li = Li()
            temp_li.populate(link)
            self.external_links.append(temp_li)

        for image in e_node.find("Images") or [] :
            temp_li = Li()
            temp_li.populate(image)
            self.images.append(temp_li)

        for video in e_node.find("Videos") or [] :
            temp_li = Li()
            temp_li.populate(video)
            self.videos.append(temp_li)

        for map in e_node.find("Maps") or [] :
            temp_li = Li()
            temp_li.populate(map)
            self.maps.append(temp_li)

        for feed in e_node.find("Feeds") or [] :
            temp_li = Li()
            temp_li.populate(feed)
            self.feeds.append(temp_li)

        find_summary = e_node.find("Summary")
        if find_summary :
            summary = find_summary.text

    def xml_from_li(self, root_str, item_list) :
        #Loop through list items contains in common lists
        xml_string = "<" + root_str + ">"
        for listitem in item_list :
            #assert listitem is type(Li)
            xml_string += listitem.print_xml()
        xml_string += "</" + root_str + ">"
        return xml_string

    def print_xml (self) :
        #Export xml from the common class
        self_string = ""
        if self is not None:
            self_string += "<Common>"
            if self.citations != [] :
                root = "Citations"
                xml_citations = self.xml_from_li(root, self.citations)
                self_string += xml_citations
            if self.external_links   != [] :
                root = "ExternalLinks"
                xml_external_links = self.xml_from_li(root, self.external_links)
                self_string += xml_external_links
            if self.images    != [] :
                root = "Images"
                xml_images = self.xml_from_li(root, self.images)
                self_string += xml_images
            if self.videos    != [] :
                root = "Videos"
                xml_videos = self.xml_from_li(root, self.videos)
                self_string += xml_videos
            if self.maps      != [] :
                root = "Maps"
                xml_maps = self.xml_from_li(root, self.maps)
                self_string += xml_maps
            if self.feeds     != [] :
                root = "Feeds"
                xml_feeds = self.xml_from_li(root, self.feeds)
                self_string += xml_feeds
            if self.summary is not None:
                self_string += "<Summary>" + self.summary + "</Summary"
            self_string += "</Common>" 
        #Conclude common xml instance string
        return self_string



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



