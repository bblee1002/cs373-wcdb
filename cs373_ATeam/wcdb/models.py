import os
os.environ["DJANGO_SETTINGS_MODULE"] = "cs373_ATeam.settings"
from django.db import models

"""
File containing definitions for our Django models and any relevant classes and function
"""

def populate_li(root, modl_id, tag):
    """
    Function expects a root, model ID, and tag as parameters. Tag is used to look traverse 
    the root's tree and find the correct parameters to pass to Li's populate method.Once an 
    Li object is populated, the function saves it to the database
    """
    outer_node = root.find(tag)
    if outer_node is not None:
        for li in outer_node or [] :
            href = li.get("href")
            embed = li.get("embed")
            text = li.get("text")
            floating_text = li.text

            if href is None:
                href = ''
            if embed is None:
                embed = ''
            if text is None:
                text = ''
            if floating_text is None:
                floating_text = ''

            temp_li = Li()
            check = Li.objects.filter(model_id=modl_id, href=href,
                embed=embed, text=text, floating_text=floating_text, kind=tag)

            if len(check) == 0:
                temp_li.populate(li, modl_id, tag)
                temp_li.save()





class Li(models.Model) :
    """
    Class for the List tag in the unified xml schema. Contains a field for an href, embedded link, 
    and alt text. The floating_text attribute is to catch any text not in attributes.
    """
    #Li
    href          =  models.CharField(max_length=2000)
    embed         =  models.CharField(max_length=2000)
    text          =  models.CharField(max_length=2000)
    #text not in the attributes; not Li
    floating_text =  models.CharField(max_length=4000)
    model_id      =  models.CharField(max_length=200)
    kind          =  models.CharField(max_length=200)
    #only if type is citation



    def populate(self, e_node, modl_id, item_type) :
        """
        Non-static method expects an element node, model id, and an Li type as parameters. Example 
        values for type: citations, videos, images, etc. Uses node to populate attributues of a Li 
        object.
        """

        if e_node.get("href") is not None:
            self.href          =  e_node.get("href")
        if e_node.get("embed") is not None:
            self.embed         = e_node.get("embed")
        if e_node.get("text") is not None:
            self.text          =  e_node.get("text")
        if e_node.text is not None:
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
    # def __init__(self):
    #     self.citations      = []
    #     self.external_links = []
    #     self.images         = []
    #     self.videos         = []
    #     self.maps           = []
    #     self.feeds          = []
    #     #similar to floating text
    #     #self.summary        = None

    def populate(self, e_node, modl_id) :
        """
        Non-static method expects an element node and model ID as a parameter.
        Uses node to populate attributues of a Common object
        """
        populate_li(e_node, modl_id, "Citations")
        populate_li(e_node, modl_id, "ExternalLinks")
        populate_li(e_node, modl_id, "Images")
        populate_li(e_node, modl_id, "Videos")
        populate_li(e_node, modl_id, "Maps")
        populate_li(e_node, modl_id, "Feeds")




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

class Relations(models.Model) :
    """
    Relation model maintaining relationships between Crisis, Person, and Org models
    """
    crisis_ID = models.CharField(max_length=200)
    person_ID = models.CharField(max_length=200)
    org_ID    = models.CharField(max_length=200)
    def populate(self, c_id = None, p_id = None, o_id = None) :
        """
        Non-static method expects a crisis ID, person ID, and organization ID as optional parameters.
        """
        if c_id is not None :
            self.crisis_ID = c_id
        if p_id is not None :
            self.person_ID = p_id
        if o_id is not None :
            self.org_ID = o_id

class Crisis(models.Model) :
    """
    Crisis Model
    """
    crisis_ID         = models.CharField(max_length=200, primary_key=True)
    name              = models.CharField(max_length=200)
    kind              = models.CharField(max_length=200)
    date              = models.CharField(max_length=200)
    time              = models.CharField(max_length=200)
    #relations models
    # people            = []
    # organizations     = []
    # #Li list
    # #locations, human_impact, economic_impact is always floating text
    # locations         = []
    # human_impact      = []
    # economic_impact   = []
    # resources_needed  = []
    # ways_to_help      = []
    #common
    common            = Common()
    common_summary    = models.CharField(max_length=2000)


class Person(models.Model) :
    """
    Person Model
    """

    person_ID         = models.CharField(max_length=200, primary_key=True)
    name              = models.CharField(max_length=200)
    kind              = models.CharField(max_length=200)
    location          = models.CharField(max_length=200)
    #relations models
    # crises            = []
    # organizations     = []
    #Li list
    #locations, human_impact, economic_impact is always floating text
    #common
    common            = Common()
    common_summary    = models.CharField(max_length=2000)
        
    

class Org(models.Model) :
    """
    Organization Model
    """
    org_ID         = models.CharField(max_length=200, primary_key=True)
    name           = models.CharField(max_length=200)
    kind           = models.CharField(max_length=200)
    location       = models.CharField(max_length=200)
    #relations models
    # crises         = []
    # people         = []
    # #Li list
    # history        = []
    # contact        = []
    #Common
    common         = Common()
    common_summary = models.CharField(max_length=2000)




