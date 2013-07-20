import os
os.environ["DJANGO_SETTINGS_MODULE"] = "cs373_ATeam.settings"
from django.db import models

"""
File containing definitions for our Django models and any relevant classes and function
"""


def list_add(m_list, id) :
    """
    Function expects a list and some object
    The object is appended to the list
    """
    m_list.append(id)




class Li(models.Model) :
    """
    Class for the List tag in the unified xml schema. Contains a field for an href, embedded link, 
    and alt text. The floating_text attribute is to catch any text not in attributes.
    """
    #Li
    href          =  models.CharField(max_length=200)
    embed         =  models.CharField(max_length=200)
    text          =  models.CharField(max_length=200)
    #text not in the attributes; not Li
    floating_text =  models.CharField(max_length=200)
    model_id      =  models.CharField(max_length=200)
    kind          =  models.CharField(max_length=200)
    #only if type is citation



    def populate(self, e_node, modl_id, item_type) :
        """
        Non-static method expects an element node as a parameter.
        Uses node to populate attributues of a Li object
        """
        self.href          =  e_node.get("href")
        self.embed         = e_node.get("embed")
        self.text          =  e_node.get("text")
        self.floating_text =         e_node.text
        self.model_id      =             modl_id            
        self.kind          =           item_type


    #Check for presence of "&" invalid XML char
    def clean_li_xml (self, dirty) : 
        """
        Non-static method expects a string as a parameter.
        Searches string for ampersands and escapes them to convert them to valid xml
        """
        dirty_clean = dirty.split("&")
        for dirty_piece in dirty_clean:
            #first element case, is insures unique
            if dirty_piece is dirty_clean[0] :
                dirty_new = dirty_piece
            else :
                dirty_new += "&amp;" + dirty_piece
        return dirty_new

    def print_xml (self) :
        """
        Non-static method used to export the contents of a Li object as valid xml
        """
        self_string = ""
        if self is not None:
            if self.href is not None :
                href_clean = self.clean_li_xml(self.href)
                self_string += "<li> href=\"" + href_clean + "\"</li>"
            if self.embed is not None :
                embed_clean = self.clean_li_xml(self.embed)
                self_string += "<li> embed=\"" + embed_clean + "\"</li>"
            if self.text is not None :
                text_clean = self.clean_li_xml(self.text)
                self_string += "<li>" + text_clean + "</li>"
            if self.floating_text is not None :
                floating_text_clean = self.clean_li_xml(self.floating_text)
                self_string += "<li>" + floating_text_clean + "</li>"
        #Conclude li xml instance string
        return self_string



class Common() :
    """
    Class for the Common tag in the unified xml schema Contains a field for an href, embedded link, and alt text
    The floating_text attribute is to catch any text not in attributes.
    """
    #Common
    def __init__(self):
        self.citations      = []
        self.external_links = []
        self.images         = []
        self.videos         = []
        self.maps           = []
        self.feeds          = []
        #similar to floating text
        #self.summary        = None

    def populate(self, e_node) :
        """
        Non-static method expects an element node as a parameter.
        Uses node to populate attributues of a Common object
        """
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


        # find_summary = e_node.find("Summary")
        # if find_summary is not None :
        #     self.summary = find_summary.text


    def xml_from_li(self, root_str, item_list) :
        """
        Non-static method expects a root string and a list of Li objects as parameters.
        Iterates through list of Li objects and calls their xml_from_li() method, 
        concatenating the output to a string. The root string is concatenated around this string.
        """
        #Loop through list items contains in common lists
        xml_string = "<" + root_str + ">"
        for listitem in item_list :
            #assert listitem is type(Li)
            xml_string += listitem.print_xml()
        xml_string += "</" + root_str + ">"
        return xml_string

    #Export xml from the common class
    def print_xml (self) :
        """
        Non-static method used to export the contents of a Common object as valid xml
        """
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
                self_string += "<Summary>" + self.summary + "</Summary>"
            self_string += "</Common>" 
        #Conclude common xml instance string
        return self_string



class Crisis(models.Model) :
    """
    Crisis Model
    """
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
    common_summary    = models.CharField(max_length=2000)


class Person(models.Model) :
    """
    Person Model
    """

    person_ID         = models.CharField(max_length=200)
    name              = models.CharField(max_length=200)
    kind              = models.CharField(max_length=200)
    location          = models.CharField(max_length=200)
    crises            = []
    organizations     = []
    #Li list
    #locations, human_impact, economic_impact is always floating text
    #common
    common            = Common()
    common_summary    = models.CharField(max_length=2000)
        
    

class Org(models.Model) :
    """
    Organization Model
    """
    org_ID         = models.CharField(max_length=200)
    name           = models.CharField(max_length=200)
    kind           = models.CharField(max_length=200)
    location       = models.CharField(max_length=200)
    crises         = []
    people         = []
    #Li list
    history        = []
    contact        = []
    #Common
    common         = Common()
    common_summary = models.CharField(max_length=2000)




