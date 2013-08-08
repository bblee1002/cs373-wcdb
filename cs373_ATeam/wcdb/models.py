import os
os.environ["DJANGO_SETTINGS_MODULE"] = "cs373_ATeam.settings"
from django.db import models

"""
File containing definitions for our Django models and any relevant classes and
function.
"""

def make_map_embed_string(map_string) :
    """
    Helper function for populate_li - takes in an embed string from Li objects
    of the "Maps" kind and produces the correct string for the embedded link

    @type map_string: string
    @param map_string: embed attribute from a list item of "Maps" type

    @rtype: string
    @return: The corrected version of the map's embed string
    """

    if map_string is None :
        return ''

    if map_string[0:23] == "https://maps.google.com":
        if map_string[-5:] != "embed" :
            map_string = map_string + "&output=embed"
    elif map_string[0:17] == "http://google.org" and map_string [-13:] != "embedded=true":
        map_string = map_string + "?&embedded=true"
    elif map_string[0:25] == "http://www.bing.com/maps/" and map_string[0:31] != "http://www.bing.com/maps/embed/":
        map_string = "http://www.bing.com/maps/embed/" + map_string[25:]
    else :
        map_string = ''

    return map_string

def make_video_embed_string(video_string) :
    """
    Helper function for populate_li - takes in an embed string from Li objects
    of the "Videos" kind and produces the correct string for the embedded link.

    @type video_string: string
    @param video_string: embed attribute from a list item of "Videos" type

    @rtype: string
    @return: The corrected version of the video's embed string
    """

    if video_string is None :
        return ''

    if (video_string[0:23] != "http://www.youtube.com/" or video_string[23:27] == "user") and video_string[0:18] != "//www.youtube.com/" :
            video_string = ''
    elif video_string[0:23] == "http://www.youtube.com/" and video_string[0:28] != "http://www.youtube.com/embed" :
        if video_string[23:54] == "watch?feature=player_detailpage" :
            video_string = "//www.youtube.com/embed/" + video_string[57:68]
        elif video_string[23:52] == "watch?feature=player_embedded":
            video_string = "//www.youtube.com/embed/" + video_string[55:66]
        elif video_string[23:28] == "watch" :
            video_string = "//www.youtube.com/embed/" + video_string[31:42]
        else:
            video_string = ''

    return video_string

def populate_li(root, modl_id, tag):
    """
    Helper method for loadModels.py and for Li.populate(). Creates an Li()
    object, populates it with information using a node in the tree produced
    by ElementTree, and then saves it to the database.

    @type root: ElementTree Element
    @param root: Node in parsed tree that contains list items
    @type modl_id: string
    @param modl_id: Crisis, Person, or Org with which root is associated
    @type tag: string
    @param tag: The type of node root is

    @return: No return value
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

            if tag == "Videos" :
                embed = make_video_embed_string(embed)

            if tag == "Maps" :
                embed = make_map_embed_string(li.get("embed"))

            li.embed = embed
            temp_li = Li()
            check = Li.objects.filter(model_id=modl_id, href=href,
                embed=embed, text=text, floating_text=floating_text, kind=tag)

            if len(check) == 0:
                if (tag == "Videos" or tag == "Maps") and embed == '':
                    pass
                else:
                    temp_li.populate(li, modl_id, tag)
                    temp_li.save()

class Li(models.Model) :
    """
    Class for the List tag in the unified xml schema. Represents objects in
    lists.
    @type href: models.CharField(2000)
    @cvar href: URL to which object should hyperlink
    @type embed: models.CharField(2000)
    @cvar embed: URL to be used to embed the object
    @type text: models.CharField(2000)
    @cvar text: Text associated with the object
    @type floating_text: models.CharField(10000)
    @cvar floating_text: Text to be displayed with object
    @type model_id: models.CharField(200)
    @cvar model_id: Identifies the Crisis/Person/Org object this Li is associated with
    @type kind: models.CharField(200)
    @cvar kind: The type of this Li object
    """

    # Attributes
    href          =  models.CharField(max_length=2000)
    embed         =  models.CharField(max_length=2000)
    text          =  models.CharField(max_length=2000)
    # Text between tags
    floating_text =  models.CharField(max_length=10000)

    model_id      =  models.CharField(max_length=200)
    kind          =  models.CharField(max_length=200)

    def populate(self, e_node, modl_id, item_type) :
        """
        Non-static method expects an element node, model id, and an Li type as parameters. Example 
        values for type: citations, videos, images, etc. Uses node to populate attributues of a Li 
        object.
        """
        if e_node.get("href") is not None:
            self.href          =  e_node.get("href")
        if e_node.get("embed") is not None:
            self.embed         =  e_node.embed
        if e_node.get("text") is not None:
            self.text          =  e_node.get("text")
        if e_node.text is not None:
            self.floating_text =         e_node.text
        self.model_id      =             modl_id
        self.kind          =           item_type

class Common() :
    """
    Class for the Common tag in the unified xml schema. Used as a helper class
    to create Li objects for a Crisis/Person/Org.
    """

    def populate(self, e_node, modl_id) :
        """
        Creates Common-type Li objects for a person/crisis/org, populates them,
        and adds them to the database.

        @type self: Common
        @param self: This Common instance
        @type e_node: ElementTree Element
        @param e_node: A child of a Common Element that has list item children.
        @type modl_id: string
        @param modl_id: ID that uniquely identifies a person, crisis, or org.

        @return: No return value
        """

        populate_li(e_node, modl_id, "Citations")
        populate_li(e_node, modl_id, "ExternalLinks")
        populate_li(e_node, modl_id, "Images")
        populate_li(e_node, modl_id, "Videos")
        populate_li(e_node, modl_id, "Maps")
        populate_li(e_node, modl_id, "Feeds")

class Relations(models.Model) :
    """
    Represents a relationship between Crisis, Person, and Org models

    @type crisis_ID: models.CharField(200)
    @param crisis_ID: ID that uniquely identifies a Crisis object
    @type person_ID: models.CharField(200)
    @param person_ID: ID that uniquely identifies a Person object
    @type org_ID: models.CharField(200)
    @param org_ID: ID that uniquely identifies an Org object
    """

    crisis_ID = models.CharField(max_length=200)
    person_ID = models.CharField(max_length=200)
    org_ID    = models.CharField(max_length=200)

    def populate(self, c_id = None, p_id = None, o_id = None) :
        """
        Initializes the values of the class variables for a Relations object.

        @type self: Relations
        @param self: This Relations instance
        @type c_id: string
        @param c_id: A crisis ID that uniquely identifies a crisis
        @type p_id: string
        @param p_id: A person ID that uniquely identifies a person
        @type o_id: string
        @param o_id: An org ID that uniquely identifies an organization

        @return: No return value
        """
        if c_id is not None :
            self.crisis_ID = c_id
        if p_id is not None :
            self.person_ID = p_id
        if o_id is not None :
            self.org_ID = o_id

class Crisis(models.Model) :
    """
    Crisis Model - represents a crisis

    @type crisis_ID: models.CharField(200, primary_key = True)
    @param crisis_ID: ID which uniquely identifies a crisis
    @type name: models.CharField(200)
    @param name: Name of the crisis
    @type kind: models.CharField(200)
    @param kind: The kind of crisis
    @type date: models.CharField(200)
    @param date: The date when the crisis began
    @type time: models.CharField(200)
    @param time: The time at which the crisis began
    @type common_summary: models.CharField(10000)
    @param common_summary: A summary of the crisis
    """
    crisis_ID         = models.CharField(max_length=200, primary_key=True)
    name              = models.CharField(max_length=200)
    kind              = models.CharField(max_length=200)
    date              = models.CharField(max_length=200)
    time              = models.CharField(max_length=200)
    common_summary    = models.CharField(max_length=10000)
    def getID(self) :
        """
        Gets the ID associated with this Crisis object

        @type self: Crisis
        @param self: This Crisis instance

        @rtype: string
        @return: The ID associated with this Crisis instance
        """

        return self.crisis_ID


class Person(models.Model) :
    """
    Person Model - represents a person

    @type person_ID: models.CharField(200, primary_key = True)
    @param person_ID: ID which uniquely identifies a person
    @type name: models.CharField(200)
    @param name: Name of the person
    @type kind: models.CharField(200)
    @param kind: The kind of person
    @type location: models.CharField(200)
    @param location: Where the person is currently located
    @type common_summary: models.CharField(10000)
    @param common_summary: Information about the person
    """

    person_ID         = models.CharField(max_length=200, primary_key=True)
    name              = models.CharField(max_length=200)
    kind              = models.CharField(max_length=200)
    location          = models.CharField(max_length=200)
    common_summary    = models.CharField(max_length=10000)
    def getID(self) :
        """
        Gets the ID associated with this Person object

        @type self: Person
        @param self: This Person instance

        @rtype: string
        @return: The ID associated with this Person instance
        """

        return self.person_ID
        
    

class Org(models.Model) :
    """
    Organization Model - represents an organization

    @type org_ID: models.CharField(200, primary_key = True)
    @param org_ID: ID which uniquely identifies an organization
    @type name: models.CharField(200)
    @param name: Name of the organization
    @type kind: models.CharField(200)
    @param kind: The kind of organization
    @type location: models.CharField(200)
    @param location: Where the organization is currently located
    @type common_summary: models.CharField(10000)
    @param common_summary: Information about the organization
    """
    
    org_ID         = models.CharField(max_length=200, primary_key=True)
    name           = models.CharField(max_length=200)
    kind           = models.CharField(max_length=200)
    location       = models.CharField(max_length=200)
    common_summary = models.CharField(max_length=10000)
    def getID(self) :
        """
        Gets the ID associated with this Org object

        @type self: Org
        @param self: This Org instance

        @rtype: string
        @return: The ID associated with this Org instance
        """

        return self.org_ID




